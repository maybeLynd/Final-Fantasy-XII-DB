# SWE2-AUDIT-SEM review — SWE2-DATA's f7a3292bd leftovers: SD-24, the input-channel base, G-2 / G-11 / G-13 / AP-6 corrections (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `DATA-REQ-AUDITSEM-DD-LEFTOVERS-0930` (T1) |
| reviewed | `5d9b11599` (author **SWE2-DATA**) — [`dd-leftovers-0930/README.md`](../dd-leftovers-0930/README.md), `sd24_record.py`, `in_channel_base.py` |
| image / data | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8`; every shipped `.sab` |
| **verdict** | **ACCEPT** |

## 1. Producer checkers re-run (SWE2-AUDIT-SEM)

`sd24_record.py` and `in_channel_base.py`: exit 0, `FAILS 0`, identical outputs ([`producer_rerun.out`](producer_rerun.out)).
The X control is sensitive as claimed: 0 of 11,165 records key validly under the rejected reading.

## 2. Re-read from the image (SWE2-AUDIT-SEM)

[`ddl_own.py`](ddl_own.py), [out](ddl_own.out).
- **SD-24.** Walker `007E681D mov rax, [rdi+0x30]` is paired with `007E6828 lea rax, [01CB43E0]`. That vtable's
  CompleteObjectLocator (`01D3F7E0`, signature 1, self-RVA valid) names **`.?AVSound@SabFile@Sd@SQEX@@`**. The bind
  `007BDDDD mov rax, [rdx+0x18]` / `007BDDE1 mov [rcx+0x30], rax` stores the record, and `007BDE4E movzx eax, byte
  [rax+0x4E]` reads past a 64-byte `Sequence`, as R3 says. `this+0x30` is the sound's `SabFile::Sound` record.
- **The channel base.** `0035F2A8 lea rdi, [022CAE91]` and `0035F2E3 lea rbx, [rdi-1]` (= R `022CAE90`). The
  initialiser's `0035F31D mov word [rdi+0xA], 0x90` and `0035F323 mov byte [rdi+0xC], 0x20` land at R+0x0B and
  **R+0x0D**, and the analog builder reads the dead-zone radius at `0035F7BD movzx edx, byte [rsi+0xD]`. So AP-6's "never
  writes `+0x0D`, dead-zone radius 0" was wrong, and the corrected value `0x20` is right.

## 3. Strikes and consumers (questions 2 and 4) (SWE2-AUDIT-SEM)

A grep over the database pages and TSVs for the dead-zone claim finds it only struck, with the dated correction, on
the input-stack page (§5) and in the AP-6 row. The other hits are this record and DATA's inbox. For the `+0x24` key /
`Sequence`-container reading, the remaining current hits are the 2026-09-12 profile of the `Sequence` records on the
sound page (§7, lines ~330–336) and in FABLE's inbox. Both describe `Sequence` bytes genuinely and make no container
claim, so they agree as the record says. The G-2, G-11 and G-13 rows were read at HEAD: the struck phrases are the
old texts, and the corrections say no more than R1–R4 and D1–D3 show. The routed `ff12config` line (to FABLE) and the
derived crosswalk and snapshot (to FRONTIER) are correctly left unedited.

## 4. The reporter's UNKNOWN row (question 5) (SWE2-AUDIT-SEM)

Re-running the record's helper at HEAD gives no UNKNOWN row (WITHDRAWN 181, ANSWERED 1513, OPEN 26, PARTIAL 6; the
unidentified register is empty). ANSWERED has moved by one since the record's run, from register traffic. One
limit: the helper, `Tools/work/SWE2-DATA/dd/unknown_rows.py`, is gitignored. The item-4 finding therefore rests on an
untracked script, the same class as the DD-rule T gap (`auditsem-review-ddrule-t-0930`). It is a small check and
this re-run confirms it, but the script belongs under the record folder.
