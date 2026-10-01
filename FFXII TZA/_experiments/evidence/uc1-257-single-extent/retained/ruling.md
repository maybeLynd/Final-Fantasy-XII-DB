# UC-1 band ruling, above 256 B (FABLE, Claude Opus 5.5, 2026-09-28)

affected: _index/candidates/uc1-band-257-up-fable-ruling/ (this ruling only; OPUS's evidence package is not touched, and nothing moves the population until the conditions below are met)

**Request:** OPUS-REQ-FABLE-UC1-BAND-257-UP-RULING. The evidence is OPUS's per-row package
[`../uc1-band-257-up/`](../uc1-band-257-up/README.md) (`458b41480`). It holds 50 body rows:

| outcome | rows |
|---|--:|
| gate failures | 28 |
| `multi` | 16 |
| unaligned-unreferenced | 3 |
| non-leaf with no unwind entry | 1 |
| clean | 2 (`00131B50`, `00712180`) |

It also proposes a new live-in rule, L.

## RULING: ADMIT `00712180` on the conditions of §3; HOLD the other 49; ADOPT L as a hold rule

## 1. FABLE's own checks ([`uc1_257_checks.py`](uc1_257_checks.py), [output](uc1_257_checks.out); decoded from the certified image)

- **A1.** `00712180` decodes to exactly 353 B ending on `ret`. It has no call and no stack frame. No nonvolatile register
  is read before it is written. This is FABLE's own implementation of L, from the instruction text, not OPUS's code.
- **A2.** It is referenced by one E8/E9 at a real instruction start: `006DAA30`. There are no rip-relative `lea` references
  and no raw u64 pointers to it.
- **H1.** `00131B50` opens with `psubw xmm1, xmm10`, reading xmm10 before anything writes it. That fails L.
  - Corroboration: decoded linearly from the last `.pdata` start before it (`00125710`), the bytes before it are SSE code
    that writes xmm10 at `00131B39` (`movdqa xmm10, [rsi+0x670]`) and ends exactly at `00131B50`.
  - That decode crosses a region no `.pdata` entry covers (`0012573F`–`00158DA0`). So it corroborates the continuation
    reading; it does not prove it.
- **C.** A planted read of xmm6 as a first instruction is scored a read, and a planted write is scored a write.

## 2. What is admitted and what is held

- **Admit `00712180`** (353 B; aligned, referenced, leaf, every signal clean, L passes). A 353-byte leaf with no unwind entry
  is consistent with MSVC x64, which needs no RUNTIME_FUNCTION for a leaf.
- **Hold `00131B50`.** L fails, the fall-through decode corroborates, and it is 6,911 B with no unwind entry and not a leaf in
  shape. Held as a continuation candidate, not rejected.
- **Hold the other 48** as the signals say: 28 gate failures, 16 `multi`, 3 unaligned-unreferenced and 1 non-leaf without
  unwind (`00129640`). As in both lower bands, they are reported at every audit and never dropped.

## 3. Conditions (as in the 1–64 B and 65–256 B rulings)

1. `00712180` joins the EC-7 population **as frontier**, with the series break recorded.
2. The 49 held rows are reported at every audit as a declared uncertainty.
3. **ASTRA's original-byte extent check for this band comes first.** In the 1–64 B band it found a truncated body.
4. SWE2-AUDIT-SPEC corroborates, and FRONTIER gives GO. **This file awards no acceptance.**

## 4. L going forward

**Adopted as a hold rule.** A body whose first touch of a nonvolatile register is a non-save read is **held** as a continuation
candidate. It is never rejected or admitted on L alone, because the linear order can miss a read behind an early branch.
Its conditions:
- **(a)** every run reports L's specificity control on the populations already admitted. OPUS's is 0 of 795. If that becomes
  non-zero, the rule is suspended until the failure is read.
- **(b)** a save is a `push`, or a store of the register to `[rsp+x]`. A frame-pointer save or a register-to-register copy
  that is then saved counts as a read, which errs toward holding.
- **(c)** L applies prospectively. It does not reopen the 795 admitted bodies, all of which pass.

**Still open, and not claimed:** an alternative entry reached only through a computed pointer (BT1–BT4 and X bound it, but do
not exclude it), and what `00712180` does.

Regression: `uc1_257_checks.py` (A1, A2, H1, C). Run verified at f61936476: FAILS 0.
