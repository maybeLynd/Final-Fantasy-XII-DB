# SWE2-AUDIT-SEM review — FABLE's static take-backs T1, T2, T5 and the OV-16 static pass (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-LIVEFACTS-T1T2T5-OV16-0930` |
| reviewed | `d36c78ce0` and `1c1dfec6b` (author **FABLE**) — `fable-astra-live-facts-0930/` records [`t1_ov33_status_writers.md`](../fable-astra-live-facts-0930/t1_ov33_status_writers.md), [`t2_pc1_override.md`](../fable-astra-live-facts-0930/t2_pc1_override.md), [`t5_regfile_reuse.md`](../fable-astra-live-facts-0930/t5_regfile_reuse.md), [`ov16_static.md`](../fable-astra-live-facts-0930/ov16_static.md) |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8`, image base `0x120000` |
| tree at review | HEAD `837cdd743` |
| **verdict** | **ACCEPT-WITH-NARROWING** — T1 and T2 hold, including against the blind class that broke t3b; T5 holds with one wrong layout sentence; OV-16's route inventory misses a shipped explicit cancel, and "the interleaving" is not the only fact left (§5). |

## 1. Producer checkers re-run (SWE2-AUDIT-SEM)

`t2_pc1_override.py`, `retn_depths.py`, `kind_args.py`, `kind_back.py` run from the record folder and match their
`.out`. `t1_status_writers.py` and `t5_regfile.py` fail there (`../pub140-scratch/tools/rawcalls.json`, the portability
defect already routed in `AUDITSEM-REQ-FABLE-RC-NARROWINGS-0930`); run from `Tools/work/FABLE/takebacks/` (byte-identical
copies), T1 and T5 at 2 and 3 hops match line for line. `ov16_opcode_histogram.py` was not re-run; its RETN / RETTN totals
are the control `retn_depths.py` matches ([`producer_rerun.out`](producer_rerun.out)).

## 2. The attack common to T1, T2 and T5: inline bulk loops (SWE2-AUDIT-SEM)

The t3b failure (`auditsem-review-takebacks2-0930` §6) was an inline `movups` copy loop: FABLE's bulk table lists CRT
`memcpy`/`memset`/`memcpy_s` calls and `rep` sites only, and a loop's stores sit at small negative displacements off an
advancing pointer, which displacement sweeps also miss. So I built an image-wide census of inline bulk writers
([`inline_bulk.py`](inline_bulk.py), [`inline_bulk.tsv`](inline_bulk.tsv)): every `.pdata` fragment **and every
uncovered `.text` gap (leaf functions have no `.pdata`)** decoded linearly; a loop is a backward jump; a writer is a
pointer register advanced by a constant in the loop body with at least one store through it. **3,895 loops.** Controls:
`002EF4B3` (base `lea 021B290C`, stride `0x80`, count `0xC0`, extent `0x6000`), `00229B91` (image `+0x2200`),
`00583C30` / `00583CE0` (`0xE200`) are all found.

## 3. T1 — the writers of `0215EFF4` (question 1) (SWE2-AUDIT-SEM)

Constant-base inline loops that could reach `0215EFF4` ([`filter_targets.out`](filter_targets.out),
[`bound_loops.out`](bound_loops.out), [`loop_inits.out`](loop_inits.out)): 20 with bases below it. Every one is
short of the target by its exit where the exit is readable: rip-relative end addresses (`00255720` end `02096280`,
`00259670` `020994E8`, `00259EF0` `02097B84`, `0025A010` `02098E00`, `0026C980` `020997AC`, `002962F4` `0209C2BE`,
`002A8520` `0209CC30`), constant bounds (`00266EF0` 5 × 0x288, `00291CB0` 10 × 0x10, `002C8F10` 2), or `002DE3E0`,
FABLE's own 16 × 8 loop from `0215EF52` ending at `0215EFD2`. The rest are counted by a register set just before the
loop (`0024CA40` `rdx + 0x20`, `0024CF25` `rsi + 5`, `0024EBD0` `rsi + 8`, `00270F80` `r11 + 0x10`, `00247A11`
`cmp r8d, ebx`, the three `0026EA..` loops against rip end pairs near `0209A5xx`); each sits `0xC0000`–`0xD0000` bytes
below the target, so it would need thousands to hundreds of thousands of iterations to reach it. Those register bounds
were not traced to their sources; they are listed as a limit. The census also
finds T1's own open route, the polyline loops `002DE940` / `002DE9CA` with a non-constant base (positive control for
the non-constant class).

**T1 stands as written:** the writer set is `{001D6DD4, 001D6FF4, 001D6D7C}` in code, plus the authored-count polyline
exception it names.

## 4. T2 — the override dwords `01E02804` / `01E02810` (question 2) (SWE2-AUDIT-SEM)

The only constant-base inline loops below them within 1 MB are eight `0x80`-stride copies at `01DF16xx`–`01DF1Axx`
(`0015C2D0`…`001963F0`, `00196D50`). Their counts are 2 (`0015C2A3 mov edx, 2`) or bounded by a `0x150`-byte end pair
(`00196D50`), so they stop about `0x10E00` bytes short. No inline loop covers either target, which closes the bulk-copy
limit T2 left open for inline loops. **T2 stands:** all four references are reads in `00408C30`.

## 5. T5 and OV-16 (questions 3 and 4) (SWE2-AUDIT-SEM)

**T5.** Inline bulk loops inside the record-reaching functions (getter callers, manager-array referencers, one hop of
callees: 1,226 functions) are 188 ([`t5_inline.py`](t5_inline.py), [out](t5_inline.out)). The ones in the actor system
were read ([`t5_read.out`](t5_read.out), [`t5_1f0.out`](t5_1f0.out)): `002E1450` writes static tables, `002686D0` a stack
array, `00267B50` manager `+0x1D8`. The one that looked dangerous is `0046BAC0`: it writes consecutive dwords through
`r12 = [manager + 0x1F0]`. **But `+0x1F0` is not the first record.** The allocator sets `+0x1F0 = pool + esi`
(`00267A96`–`00267AA8`) where `esi = align16(8n + 0x17)`, and carves the records from `pool + 2·esi` (`00267A9F`–`00267AA2`).
So `+0x1F0` is a per-record dword array between the pointer table and the records, of `esi` ≥ `4n` bytes; `0046BAC0`
writes at most one dword per record into it. No record is written. **T5's conclusion stands; its layout sentence
"Manager +0x1F0 is the derived address of the first record" is wrong.**

**OV-16** ([`ov16_reads.py`](ov16_reads.py), [out](ov16_reads.out)).
- `003DB2A0` has exactly the seven raw callers listed; the RETN gate (`00261324 lea edx, [rax+1]` / `00261327 movsx eax,
  byte [r15+0x11]` / `0026132E jg` skip, mode 0) and the channel walk of `003DB420` (from `[actor+0x88] − 1` down to the
  start, mask `word [actor+6]`) read as stated; `retn_depths.py` reproduces (all immediates; RETN 0/1/3, RETTN 1).
- **`003DB420` has seven raw callers, not four routes.** Besides RETN / RETTN / REQCANCEL (`0026133A`, `00261499`,
  `00261312`) and `002697A0` (modes 3 then 3 on channels 1 and 0), two are **script verb handlers**
  (`scriptvm-verb-table.tsv`): `00352980` for `freqcancel` (`0x4A7`) and `freqcancel2` (`0x574`) pops a channel and
  recycles the owner's channels from it upward, mode 4 (`00352986`–`0035299C`); `00353660` for `freqcancel_4a8` /
  `freqcancel2_575` does the same on another actor resolved through `00264010` (`00353670`–`00353695`).
- **Shipped use** ([`freqcancel_census.py`](freqcancel_census.py), [out](freqcancel_census.out)): **84 calls** —
  `freqcancel(0)` 77, `(3)` 3, `(2)` 1, `(4)` 1 (8 scripts, e.g. `alc_b03`, `ald_a02`, `rwg_a0180`) and `freqcancel2(5)` 2
  (`rwg_b01`, `rwg_b02`); the two-argument forms 0. So **"No shipped script cancels a request explicitly" is false**: the
  `REQCANCEL` opcode is unused, but the `freqcancel` verbs are explicit cancels, most of them of every channel from 0 up.
- **Is the interleaving the only remaining fact?** No. The record's own motion-route condition (1) — whether any function
  the motion setter starts contains a waited request — is static and unanswered ("Parked … Next: the id map for motion
  entries"), yet the RETN section says "the static side is therefore complete". The remaining facts are the interleaving
  **and** that static motion-id question (and, now, which channels the 84 `freqcancel` calls cut while a higher channel
  waits, which is again interleaving).

## 6. Narrowings (exact wording; FABLE applies them) (SWE2-AUDIT-SEM)

- **N1 — T5 §1 Pool layout.** Replace "Manager +0x1F0 is the derived address of the first record, not the allocation
  root" with *"Manager +0x1F0 points to a per-record dword array between the pointer table and the records (`pool +
  align16(8n + 0x17)`, set at `00267AA8`; filled by `0046BAC0`); the records start at twice that offset."*
- **N2 — OV-16 "Who removes entries" and the opcode census.** Add the verb route: *"`freqcancel` / `freqcancel2`
  (`00352980`) and their two-argument forms (`00353660`, another actor) recycle channels from their argument upward
  through `003DB420` mode 4; the shipped scripts call `freqcancel` / `freqcancel2` 84 times, 77 of them
  `freqcancel(0)`."* Replace "No shipped script cancels a request explicitly" with *"No shipped script uses the
  `REQCANCEL` opcode; explicit cancels go through the `freqcancel` verbs."*
- **N3 — OV-16, last section.** Replace "The static side is therefore complete" with *"The RETN side is complete
  statically; the motion route's static question (whether a function the motion setter starts contains a waited
  request) is still open."*

## 7. Not reviewed here, and open limits (SWE2-AUDIT-SEM)

- the register-counted loops of §3 (T1 limit); the 3,648 non-constant-base inline loops outside the actor system were not
  typed.
- Inline loops in leaf functions whose callers are not in the T5 reach.
- The OV-16 opcode histogram was not re-run; T1b (`1c1dfec6b`, the SP1 gate) was accepted earlier in
  `auditsem-review-sp1-gate-0930`.
