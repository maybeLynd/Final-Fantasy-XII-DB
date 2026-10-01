# SWE2-AUDIT-SPEC review of SD-6 (sd6-recorded-input-0930 at 60e34af0e): ACCEPT

Reviewer: SWE2-AUDIT-SPEC (non-author; Claude Opus 5.5, session 73162e75, 2026-09-30). Reviewed: OPUS's
`60e34af0e` (the record's only commit), [README](../sd6-recorded-input-0930/README.md) and `sd6_input_source.py`, plus
the shared lookup tool `Database/Tools/analysis-kit/gfz-scripts/retool.py` it uses. Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-SD6-0930 | sd6-recorded-input-0930 | `60e34af0e` | ACCEPT |

**Re-run.** `sd6_input_source.py` re-run at HEAD from its own directory: [rerun_sd6_input_source.out](rerun_sd6_input_source.out)
is identical to the committed `.out` (ignoring CR), F1-F8 and C1 PASS, `FAILS 0`. The record directory stayed clean.

**Re-derived independently** ([sd6_rederive.py](sd6_rederive.py) / [.out](sd6_rederive.out)). This uses tk.py's raw sweep of
ALL `.text` bytes, not retool.py's extent-bounded function list, plus the image-base-relative form, relocations and an
unaligned raw-qword scan.
- The gate `[02EA5220]` has 1 rip reference, a read `0079F1CF` in `0079F150`. The gate `[02EA5230]` has 1, a read
  `0079F2EB` in `0079F150`. Neither has an image-base-relative reference. There are 0 relocations and 0 raw qwords
  pointing into `02EA5210`..`02EA5237`.
- Both gates lie past `.data`'s raw bytes, which end at `01F7E400`, so they are zero-initialised.
- The table and count (`02EA5480`..`02EA548F`) have 24 rip references, in only three owners:
  - the run loop `00796490`: reads, plus stores at `007965C4`/`007965CB`/`007965FD`/`00796604`;
  - the teardown `008B7B90`: stores at `008B7BBF`/`008B7BC6`;
  - the loader `0079FB10`: reads, plus the one address-take `lea` at `0079FC78`.

  Two raw-only candidates in `001692E0` are not accesses: `00169305` reads `02EA547C`, a neighbouring dword.
- Across `02EA4100`..`02EA522F`, every rip write or `lea` targets the control byte `02EA5213`. There are 7 of them.
- Callers, from `rawcalls.json` plus a whole-`.text` `0F 8x` jcc sweep plus rip references:
  - `0079FB10` has 1 caller, `00797A20` at `00797AAD`. `00797A20` has no call site; its one reference is the
    `lea` at `007A0298` in the registrar `007A0180`.
  - `007A0180` has 2 callers, `00792760` and `0079F150`. `00792760` has 1, `0079F150`.
  - No jcc lands on any of the four.

  This matches F3-F6 exactly.

**Controls.**
- C1 (`02EA5213` written at `00799137`) is sensitive to the defect it guards against, a blind reference scan: my
  whole-image sweep finds 7 writers/`lea`s of that byte, so the scan does see stores in this block.
- F7/F8 rest on retool.py's scan, which covers listed extents only and the rip form only. My sweep closes both gaps for
  these cells: it covers unlisted code and the image-base-relative form, and still finds nothing.

**retool.py (requested).** It is fit for these lookups, with four stated limits:
- Only listed extents are decoded, linearly from each start.
- Only rip-relative operands are indexed; `[reg+disp]` with an image-base register is not.
- The call index is direct `call`/`jmp` only; no jcc.
- `qword_sites` scans 8-aligned qwords only.

Its `W` classification marks any memory operand 0 that is not `cmp`/`test`/`push` as a write, so `bt [mem]` would
count as a write. None of these changes an SD-6 fact. The cache key hashes only the first 1 MiB of the image plus the
extents, which is adequate while the image is pinned by the certified hash.

**Correction wording:** none needed. The record's page correction ("`00796490` only clears it; the filler is
`0079FB10`") stands.
