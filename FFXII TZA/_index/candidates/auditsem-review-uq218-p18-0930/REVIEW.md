# SWE2-AUDIT-SEM review — SWE2-DATA's UQ-218 pass 18 (band names, yaw sign, `@FOR` tail lists, `@FDM` `+0x08`, `@FEF` table) (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30; this claim was
taken over from an earlier session of the same identity that ended without working it.*

| | |
|---|---|
| request | `DATA-REQ-AUDITSEM-UQ218-P18` (T1, T2 aspects: the ANSWERED status and the `@FOR` "no reader" correction) |
| reviewed | `29436f1ad` (author **SWE2-DATA**) — [`uq218-pass18-0930/README.md`](../uq218-pass18-0930/README.md) and its three scripts |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT-WITH-NARROWING** — the five answers stand and the `@FOR` correction is right; two sentences are narrower than written (§3). The ANSWERED status stands with them. |

## 1. Producer checkers re-run (SWE2-AUDIT-SEM)

`band_names.py`, `for_tail_census.py`, `fef_tables.py`: exit 0, `FAILS 0`, outputs identical to the committed ones
([`producer_rerun.out`](producer_rerun.out)).

## 2. Re-read from the image (SWE2-AUDIT-SEM)

[`uq218_own.py`](uq218_own.py), [out](uq218_own.out); [`ctx2a.py`](ctx2a.py), [out](ctx2a.out).
- **(2) op `0x09` and `s16[ctx+0x2A]`.** `00417F40` has **two arms**, split at `00417FE3 test byte [r12+4], 3`
  (`r12 = [ctx+0x368]`):
  - the **index arm** (`0041805C`–`00418087`): `word[cmd+2] >> 1` plus `movsx word [ctx+0x2A]`, the reading the record
    uses;
  - the **name arm**: `00417FF6 mov edx, '@FMN'` → `00409930` → `00409780`, which copies the operand at `cmd+2` as a
    **string key** (`004097BC`–`004097C9`, `call 00409210`) and looks the motion up by name.

  The record does not mention the name arm. For shipped `.ca` the index reading is supported by the data control — all
  33,753 indexes land on `@FMN` entries — but that control is the only evidence for "the `+0x2A` base adds 0". No word
  store to `+0x2A` exists in the motion-command module (`00400000`–`00430000`); wider stores that cover `+0x2A` exist on
  objects not typed here. So the zero base is a data result, not a traced one.
- **(3) Yaw sign.** `004258B5`–`004258C6`: `+0x124` (facing) and the heading are scaled by `xmm8` and subtracted
  (heading − facing), wrapped, then range-tested to `00425919 mov ebx, 3` (band 3). The signed range constants were not
  decoded here; the sign conclusion rests on the producer's code read plus the corpus exclusivity (`walk_l` 287/281
  against `walk_r` 0 per band, the same for turns).
- **(4) `@FOR` list decoding.** `0053C16B movzx eax, word [rbx + r15·2 + 8]` (list base) or `0053C173 word [rbx+0xE]`
  (fourth list, when `r9d` ≠ 0); counts `0053C187 word [rbx + r15·2 + 0x10]` / `0053C18F word [rbx+0x16]`; packing kind
  `0053C227 byte [r15 + rbx + 2]` / `0053C22F byte [rbx+1]`; cursor steps `0053CDF3 add r14, 4`, `0053CDFB add rdx, 3`,
  `0053CE02 add r8, 2`. The "no reader" statement was wrong, as corrected.
- **(5) The `'h'`-class partner** is inferred from the data fit (132/132, with 59 controls that fail in their own
  `@FDM`), as the record says. It was not traced further here.
- **(6) `@FEF`.** `0019FFD0` (one `.pdata` fragment) forms **125 distinct** `PS2Data\effect_finish\jp\chara\hNNNN.efx`
  strings by rip-relative `lea`. The producer's own output agrees: 144 rows, **125 distinct companions**, 126 shipped
  `chara/h*.efx`, of which `h0000` is shipped but unnamed.

## 3. Narrowings (exact wording; SWE2-DATA applies them) (SWE2-AUDIT-SEM)

- **N1 — §1, the op `0x09` sentence.** After "the record's op `0x09` names the motion: `@FMN` index `word[cmd+2] >> 1`"
  add *"on the index arm of `00417F40` (taken when `[ctx+0x368]+4 & 3` is non-zero); the other arm looks the motion up by
  name through `00409930`/`00409780`. The `s16[ctx+0x2A]` base is shown to be 0 on the shipped `.ca` paths only by the
  33,753/33,753 data control; its writers are not traced."*
- **N2 — §5, last bullet.** Replace "all 144 models and 144 companions are shipped files" with *"all 144 models are
  shipped, and the rows name 125 distinct companion files, all shipped (`h0000.efx` ships unnamed)"*.
