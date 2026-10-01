# Review `OPUS-REQ-AUDITSPEC-REVIEW-BATCH5-R0929` — verdict: ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; producer OPUS). 2026-09-29. Review record for OPUS's batch-5
falsification pass 1 on eleven contracts, plus `CON-177`. Commits: `e02c75920`, `96294153a`, `534f58ea6`,
`8010f9b11`, `8a1889268`, `a3c8682f8`, `22b254057`, `13287a890`, `92be8b418`, `7cf074c1c`.
Image: `73461d08…21f8`. Static, Method A.

## 1. All eleven instruments re-run

Every `falsify_*.py` was re-run from its committed text at the current tree. The scripts are clean in
`git status`, and their hashes are in `rerun_summary.txt`. **All eleven outputs are identical to the
committed `.out` files** (ignoring CR). Each prints `FAILS 0`, with exit 0.

## 2. The named attack points, re-derived by instruments that are not OPUS's

| point | independent result | agrees |
|---|---|---|
| **CON-177** (steam I-1): writers of `01F83450` | rip-relative sweep: 5 sites. Stores are `0020CD71` (in `0020CD30`) and `0020CDED` (`mov qword [01F83450], 0` in `0020CD80`, right after `call 00809950` with `edx = 0x80`, a sized free). No image-base-relative disp32. `0020CD80` has one raw caller (`007986AB`); `0020CD30` has one (`0079812D`). | yes |
| steam §9 `cmp ebx, 6` | `0020CC0C cmp ebx,6 / jne`; `0020CC11 mov ebx,0x3168` … `0020CC79 add rbx,0x198` / `cmp rbx,0x3C90`. That covers 0x3168/0x198 = 31 through 0x3C90/0x198 − 1 = 37, each under the same `+0x190`/`+0x18` tests. The 7 by-id rows at `00906290` (12 B stride; the loop bound `009062E8` is 7 rows) | yes |
| steam I-4: by-index sites | 6 raw rel32 sites into `008632B0`. Four take `ecx` from `[reg + reg*4 + 0xBF0550]`, one takes `lea ecx,[rax+0x13]` (19), and `00352262` takes `ecx` from `00267E10` (a script value). None is a literal 0. I-4 is about **literals**: a script-supplied 0 at `00352262` is outside it. | yes |
| **AB-4**: arrays 24/215/215/0, 430 `.ard` | stores to `0215F0A8`: exactly `002DFA9E` and `002DFE66`. `ard_arrays.py` reads both `.data` arrays section-aware. Slot 642 begins the next table (`.bin` paths). Over slots 0..641 each array's first non-null slot is 24, with 215 `.ard` at even and 215 `.fpk` at odd slots, and 0 parity crossovers. A **separate** `.rdata` string scan finds 430 `.ard` strings, all 430 reached. | yes |
| **input word**: 51 by-name readers of `02F9736A` | `cell_access.py` (rip sweep, width- and role-aware, functions.tsv attribution). Readers by exact address: **51 functions, the identical set** to the one OPUS's instrument computes (`input_their_rd.txt`). Writers: `00253C70` ×5 word stores, plus qword stores covering the word at `002284F0`, `002498B0` and `002A329B`. | yes |
| **UI mailbox** `0215F1A0/A1/A4/A8` | writer and reader function sets match U3 exactly for all four cells. The width-aware sweep finds **no** wider or overlapping access to any of the four, and no image-base-relative forms. | yes |
| **save image**: six `0x56690` | 6 raw dword occurrences in `.text`, all decoded as the immediate: 3 are `mov r8d, 0x56690` (`002EF5FD`, `002EF65D`, `002EF718`) and 3 store the immediate to memory (`0057E42F` qword to `[rdi+0x100]`, `00581117` dword to `[rbp+7]`, `00581F2F` qword to `[rsp+0xC0]`). | yes |
| **render object** R-1: "loads" vs arithmetic uses of `0x668` | immediate uses are `mov` ×3 (`001BD527`, `001F5309`, `00897C19`), `add eax,0x668` (`00210843`) and `adc eax,0x668` (`0055C6D3`). All other raw hits are `[reg+0x668]` displacements. This is the O1 split. | yes |
| **post-processing** `[rbp + 0x108]` | `006FF900` sets `rbp` as its frame (`006FF90F lea rbp,[rax-0xA98]`) and `rsi = rcx` once (`006FF981`), never re-assigned in the 23,568-B extent. Object stores: `+0x108` only at `007009BB` and `+0x147` only at `00700083`. The `[rbp+0x108]` byte stores (`00702082`, `00702184`) are the stack local. | yes |

The CON-177 consumer check is sound. `s45-opus-replay-counters` is revised in place with the strike kept.
No other page describes `01F83450` or `0020CD30` as the one writer (by grep).

## 3. Scope of this review

- For the four contracts OPUS did not flag, I checked that the instruments reproduce but did not
  re-derive them from separate instruments: section addressing, spatial sources, music control and
  audio bank family.
- The input-word count is a **by-name** count. One more function, `002498B0`, reads the word inside a
  16-byte `movups` from `02F97360` (`00249A5E`). That is consistent with the page's "by name" wording and
  is recorded here so that no one quotes 51 as every reader.
- All sweeps here are rip-relative plus an image-base-relative disp32 check. Register-held addresses are
  outside them, as they are outside OPUS's.

## Verdict: ACCEPT

The ten surviving passes and the `CON-177` correction are supported as written. The re-measured counts
reproduce under independent instruments.

Receipts: this directory (`REVIEW.md`, `rerun_summary.txt`, `cell_access.py`, `ard_arrays.py` and
their `.out` files, `steam_mgr_cell.out`, `steam_byindex.out`, `input_their_rd.txt`).
