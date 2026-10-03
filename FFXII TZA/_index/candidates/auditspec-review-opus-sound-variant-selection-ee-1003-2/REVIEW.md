# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-sound-variant-selection-ee-1003-2)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SOUND-VARIANT-SELECTION-EE-1003-2-BEADB` · Package: `_index/candidates/opus-sound-variant-selection-ee-1003-2/` · Page: `18-Audio/Sound-Selection/sound-variant-selection.md` (commit 81c16b70b)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

Both rows were read clause by clause against the bytes. Row `007BC8D0` is exact, and so are all 10 anchors. Row `007CFD00` needs one clause replaced: it scopes the [0, 1] clamp to the normalising branch, but the bytes clamp the input for every type byte (below).

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. Output: `VERIFY 2 functions, 10 anchors`, `ALREADY`, `FAILS 0`, exit 0. `git status` on the page and the package was clean afterwards (HEAD b5028e7e9).
- `rows.json`: 2 rows, 10 anchors. Rejected 0, skipped 0, missing 0, corrections 2. Both corrections hold at the bytes: `007BCB95` writes into the `+0x88` slot, and `007CFD04` loads the header pointer.
- Semantic pass: **every row** was read against a full capstone listing of the certified image (SHA256 73461D08...).
  - `007BC8D0` (1314 B), exact. Each store was checked against the sentence.
    - `01CB5A30`, `01CB5B98` and `01CB5BA8` go to `+0/+8/+0x10`, and `01CB43E0` to `+0x28` (all `.rdata` addresses by `lea`). The qwords `+0x18/+0x20/+0x30..+0x58` and the word `+0x60` are zeroed.
    - The 0x40-slot loop runs ×4 from `+0x88`: {`01CB5A20` (`007BC963`), q`+8`, q`+0x10`, d`+0x1C`, b`+0x20`, d`+0x24`, `+0x30`=`01CB4890`, q`+0x38`=0}, ending at `jne` (`007BC976`).
    - Thirteen 0x30-slots carry `01CB44A0`: `+0x188`, `1B8/1E8/218`, `248/278`, `2A8`, `2D8`, `308/338/368/398` and `3C8`.
    - `+0x400` is zeroed twice (×4×0x40). The qwords `+0x500..+0x518/+0x528/+0x530` are zeroed, and the dword `+0x520`=-1 (`007BCB15`).
    - The second pass writes {d`+8`=0, q`+0xC`=0x3F800000 (`+0xC`=1.0, `+0x10`=0), d`+0x14`, d`+0x1C`, b`+0x20`, d`+0x24`} at exactly `88/108/148/188/1E8/2A8/2D8/308/338/368/398`. The five fields alone are written at `C8/1B8/218/248/278`, and `3C8` is not revisited.
    - The floats `+0x64..+0x7C` are 1.0 (`007BCB8E`, …). Bytes `+0x80`/word `+0x81`/`+0x83` are 0xFE (`007BCD12`), and byte `+0x3F8` is 0. `rax`=`rcx`, with no calls.
  - `007CFD00` (348 B). All clauses except the one replaced below are exact.
    - `rdx`=`[rcx+8]`. Word `+4`==0 → 0.0.
    - Type byte ≥1 (`jb`): range=`+0xC`-`+8`, and `comiss` / `ja` (`007CFD34`) → normalise, else 0.0.
    - `comiss x,0` / `jb` keeps 0 (below or unordered). Otherwise `minss x,1.0` (`01CEBBA8`, `.rdata`) (`007CFD53`).
    - The points base is `+word 2`, plus (byte`+1`+0x10)&0xF0 when the type is >3 (`ja`).
    - Binary search: signed `sar` midpoint, `ucomiss` / `je` exits on equal or unordered (`007CFDA8`), `jae` → hi=mid-1, `jle` loop.
    - The step-back runs on `jae` not taken (below or unordered) and mid>0. Otherwise `cmovge` caps at count-1 (`007CFDD8`).
    - Last point → float `+4`. Otherwise v+(v'-v)·`007A9E50`((x-k)/(k'-k), byte `+8`) (`007CFE31`).

## SWE2-AUDIT-SPEC narrowings

`007CFD00`. Replace

> when its type byte `+0` is at least 1 it normalises `xmm1` to (`xmm1` - float `+8`) / (float `+0xC` - float `+8`), returning 0.0 unless that range is above zero, then clamps the input to 0 when below 0 or unordered and to at most 1.0 (`01CEBBA8`);

with

> when its type byte `+0` is at least 1 it normalises `xmm1` to (`xmm1` - float `+8`) / (float `+0xC` - float `+8`), returning 0.0 unless that range is above zero; for every type it then clamps the input (normalised or not) to 0 when below 0 or unordered and to at most 1.0 (`01CEBBA8`);

Why: a type byte of 0 jumps from `007CFD21 jb 0x7cfd46` straight to the clamp at `007CFD46`, skipping only the normalisation. The draft's "then clamps" sits inside the type ≥1 clause.

Limits: these are body statements read from static evidence. The draft and OPUS's re-read are not independent review; this record is.
