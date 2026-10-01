# SWE2-AUDIT-SEM review — GI-2, GI-4, GI-13 answers and the eight dialog / handbook corrections (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30; this claim was
taken over from an earlier session of the same identity that ended without working it.*

| | |
|---|---|
| request | `FABLE-REQ-AUDITSEM-REVIEW-GI-DIALOGS` |
| reviewed | `4e32dd8df` (author **FABLE**) — [`gi-0929-dialogs/consumer-check.md`](../gi-0929-dialogs/consumer-check.md) and its four scripts |
| image / data | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8`; `D:/FFXII_TZA_extract` |
| **verdict** | **ACCEPT**, scoped: C1, C2 and C4 re-derived independently; C3 and C5–C8 accepted on the producer's re-run checks. |

## 1. Producer checkers re-run (SWE2-AUDIT-SEM)

`gi2_hcom_hodr.py`, `gi4_dialog_tables.py`, `gi13_saveload_states.py`, `gi4_mask800.py`: exit 0, `FAILS 0`, outputs identical
to the committed ones ([`producer_rerun.out`](producer_rerun.out)).

## 2. Independent re-derivation (SWE2-AUDIT-SEM)

[`gi_dlg_own.py`](gi_dlg_own.py), [out](gi_dlg_own.out).
- **C1, the table framing.** Read as `{u16 label, u16 help, u8 key, u8 flag}` from `00D23688`, the twelve records give
  keys 6, 5, 7, 4 (flags 1, 1, 1, 2) for the four menu rows — label `1B5F` first, i.e. Hunts = 6 in row 0 — then keys
  11–18 for the eight kind rows. The three image-base-relative uses are byte loads of the key field:
  `0056F98E movzx eax, byte [rax + rcx·2 + 0xC0368C]` (`00D2368C` = record 0 `+4`) and `00571ECE` / `005732AD` on
  `0xC036A4` (`00D236A4` = record 4 `+4`), with `rcx` = 3·index (stride 6). The dword at `00D236D0` is `80000000`, the
  next object's first dword — the retired framing's "terminator". C1 holds.
- **C2, `hcom`.** In all nine locales the file is `hcom` + header, then exactly **five** sections chained by
  `p += u16[p]` from `+8`, ending exactly at the file size (`us` 312: 52/64/96/28/64; `de/es/fr/it` 316, `in/kr/cn/ch`
  320). The size deltas sit in the second section (every non-`us` locale +4) and the fifth (`in/kr/cn/ch` +4), matching
  the record's "section-1 … every non-us locale" and "section-4 … in/kr/cn/ch" (0-based). C2 holds.
- **C4, single installers.** Image-wide, `0056F810` is referenced once (`00574D28 lea rdx` in `00574D00`) and `00556F90`
  once (`00556EF3 lea rdx` in `00556EC0`); no qword holds either. C4 holds.

## 3. Not re-derived here (SWE2-AUDIT-SEM)

C3 (`hodr` as the Den statue layout; `+0x16`/`+0x17` effect ids), C5 (`+0xFC` the decide sound), C6 (the two `bt`
masks), C7 (the `0x1D` notification classes, status at payload `+8`, the fifteen controller states) and C8 (id 31 →
Ba'Gamnan's statue) rest on the producer's named regression checks, re-run green. The routed texts to other page owners
are not reviewed here.
