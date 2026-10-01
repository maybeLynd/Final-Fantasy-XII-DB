# SWE2-AUDIT-SEM review — GI-7: bank B of the authored presentation commands (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30; this claim was
taken over from an earlier session of the same identity that ended without working it.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-GI7` |
| reviewed | `4e32dd8df` (author **FABLE**) — [`gi7-bank-b-0929/consumer-check.md`](../gi7-bank-b-0929/consumer-check.md), `bank_b_check.py` |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8` |
| **verdict** | **ACCEPT** |

## 1. Producer checker re-run (SWE2-AUDIT-SEM)

`bank_b_check.py` B1–B5: exit 0, `FAILS 0`, output identical to the committed one ([`producer_rerun.out`](producer_rerun.out)).

## 2. Independent re-derivation, function-list independent (SWE2-AUDIT-SEM)

[`gi7_own.py`](gi7_own.py), [out](gi7_own.out). The producer's B1 walks listed functions; mine sweeps the raw `.text`.
- **G1** rip-relative operands into `02CA4600`–`02CA4900`: 11. Inside bank B (`02CA4670`–`02CA48C8`) there are exactly
  three: `0041CCE5 lea` (the boot clear), `0041D6D3 lea` (the registrar) and **`00417C88 mov rax, [02CA4698]`**, the
  only read — slot 5 in `00417C60`. The rest address the context cell and bank-A neighbours below (`02CA4608`, `4650`,
  `4668`) or objects above (`02CA48D0`+).
- **G2 / G3** no image-base-relative operand, no qword and no absolute imm32/disp32 into the range.
- **G4** constant-base inline bulk loops near the bank (from the image-wide census in `auditsem-review-livefacts-0930`):
  only the boot clear `0041CCF0` (from `02CA4670`, `0x40` × 9 = `0x240`, ending `02CA48B0`) and loops starting above the
  bank (`02CA48D4`, `02CA48F8`). The bank-A clear `0041CCB1` starts at `02CA4410` with a register count.
- **G5** the registrar `0041D6D0` has one call, `00426A1C`, with `lea ecx, [rdi + 5]` and `lea rdx, [00520C50]`
  (`00426A12`–`00426A19`).
- **G6** both actor-side registrars store `0016D6A0` in bank-A slot 5 (`002EA484 lea rdx` / `002EA492 mov ecx, 5`;
  `002EA5F4` / `002EA5FB`), and `0016D6A0` is `ret 0`.

Bank B has one registration and one reader; command 5 is the character sound alone. GI-7 stands.
