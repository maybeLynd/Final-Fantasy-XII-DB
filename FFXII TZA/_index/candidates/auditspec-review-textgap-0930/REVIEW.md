# Audit-spec review: OPUS text-gap append (273 rows + 13 hand verdicts)

Reviewer: SWE2-AUDIT-SPEC · 2026-10-01 · Subject: `text-gap-append-0930`, commit `cf9a21061`
Board task: `OPUS-REQ-AUDITSPEC-TEXTGAP-APPEND-0930`

## Verdict: ACCEPT (with a forward-drift note)

## What was checked

- **Append shape.** `text-gap-citations-250.tsv` carries the dated APPENDED
  header at line 375; 273 rows follow (115 TABLE + 29 PAD + 11 UNLISTED + 118
  UNCONFIRMED — sums to 273 as claimed). Seeding/classification ran on scratch
  copies; existing rows untouched (the append block is a tail-only change).
- **Hand verdicts byte-verified on the certified image:**
  - `00129640` UNLISTED body start: int3-padded gap, `push rbp; mov rbp,rsp`
    prologue, and genuinely absent from the image's **35,713** `.pdata`
    RUNTIME_FUNCTION ranges — including the record's own count.
  - UC-1 run `0012B980..00133B40`: zero overlapping `.pdata` ranges; the
    nearest preceding range ends at `0012573F` — matching the record's exact
    figure; the six deferred addresses are correctly parked on UC-1.
  - `00148F41` cut point: body ends `repz ret` at `00148F3F`, the cite is the
    `nop dword [rax]` alignment pad — the list's recorded cut point.
  - `0036F22E` = `mov eax, edi` in the epilogue ending `ret` at `0036F23A`;
    `00808ED9` = `mov rbx,[rsp+0x40]` epilogue ending `ret` at `00808EE3`;
    `0015AE4A` = `pop r14` epilogue ending `ret` at `0015AE51`;
    `00121E11` = second byte of `jmp $` at `00121E10` after `ret` `00121E0E`.
    All four decode exactly as the (CONTRACT-narrowed) record states; none is
    data cited as code.
- **`verify_doc_addresses.py --all` re-run at HEAD:** reports **2** documents
  with pending citations, not 0 — `worldactor-scriptvm-interpreter.md` cites
  `00261DF6` and `equipment-slots-and-the-single-stat-rebuild.md` cites
  `0027C6B8`. Both citations were introduced by *later* commits (`56a49cc8c`,
  `e042d3ab8`) — the "0 pending" claim was true at `cf9a21061`. I verified both
  new cites are legitimate table data (`00261DF6` region: `66 90` pad then a
  jump-table dword run starting `0013E613`; `0027C6B8`: a small-byte switch
  index table) — they need registry rows, not corrections. Routing a request
  to OPUS to adjudicate them.

## Narrowing / notes

The forward-drift note is information only: the package's own claims all verify
at the reviewed commit; the two pending rows are the registry working as
designed.
