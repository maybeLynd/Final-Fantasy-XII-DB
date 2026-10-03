# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-battle-text-banks-ee-1003)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-BATTLE-TEXT-BANKS-EE-1003-4FEC7` · Package: `_index/candidates/opus-battle-text-banks-ee-1003/` · Page: `02-Resource-And-Asset-Pipeline/VBF-Archive-And-Authored-Tables/St2e-Carriers/battle-text-banks.md` (commit 81c16b70b)

## SWE2-AUDIT-SPEC verdict: ACCEPT

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. Output: `VERIFY 1 functions, 5 anchors`, `ALREADY`, `FAILS 0`, exit 0. `git status` on the page and the package was clean afterwards (HEAD b5028e7e9).
- `rows.json`: 1 row, 5 anchors. Rejected 1 (`0055FB20`: it names a `.text` gap and is correctly kept off the page), skipped 0, missing 0, corrections 1. The correction holds: both record loads are `mov rcx/r8, qword ptr [rip→0209CC40]` (`.data`, mutable), so the fields belong to the pointed-to record.
- Semantic pass: **every row** was read clause by clause against a full capstone listing of the certified image (SHA256 73461D08...).
  - `002B5390` (747 B), exact.
    - Null `rcx` → `xor eax,eax` → epilogue.
    - Byte `+0x27`=0. The text is `[+0x10]`, else `[+0]`. The limit is `cvtdq2ps(movsx word +0x24)`.
    - `002AC1E0(ctx)`, then `0039BAD0(rdx`, else `[+0x18])`. Its `al` goes to ctx byte `+0xA6`.
    - `rec`=`[0209CC40]`: `rec+0x10D0`=dword `+0x28`, and `rec+0x1104`=ctx byte `+0x9A` (`rsp+0xCA`).
    - `002B2150(ctx, text, &w, &x)` (`002B5449`), and `+0x28` ← `rec+0x10D0`.
    - `cvttss2si(w)` vs `cvttss2si(limit)` uses `jg` (`002B546E`). The fit path does the following:
      - Stores `+8`=text, word `+0x22`=len and `+0x26`=`text[len]`.
      - Sets `+0x10`=text+len+1, or 0 when that byte is 0.
      - Sets `+0x27`=`cmove` 2 on `rec+0x1104`==0x26, else 0.
    - `00254A10` (`002B54B1`) returning 0 gives the same stores with `or sil,1`.
    - Otherwise the prefix loop runs (the context is re-prepared each pass):
      - The chunk is `002B1FB0(text+len)` (`002B555E`), and 0 → the zero path.
      - The temporary NUL is written only when the new length is below `strlen` (`jae`). The prefix is measured with `002B2150`, then the byte is restored.
      - `comiss w,limit` / `ja` → `002B5655`: `or [+0x27],1` (`002B5655`), the length goes back by one chunk, `+8`/`+0x22`/`+0x26` are stored, and `+0x10`=break pointer (or 0 if that byte is 0).
    - The zero path clears `+8`, `+0x10`, `+0x22` and `+0x26`.
    - Every non-null path returns the value stored to `+0x10` (`rax`, or `rsi`→`rax`). The cookie is checked through `00808C40`.

Limits: these are body statements read from static evidence. The draft and OPUS's re-read are not independent review; this record is.
