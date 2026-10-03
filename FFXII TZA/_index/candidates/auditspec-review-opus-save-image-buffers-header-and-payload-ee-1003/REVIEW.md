# SWE2-AUDIT-SPEC review: OPUS interior citations (opus-save-image-buffers-header-and-payload-ee-1003)

Reviewer: FABLE (non-author, on SWE2-AUDIT-SPEC's queue at the user's request) · 2026-10-03 · Task: `OPUS-REQ-AUDITSPEC-OPUS-SAVE-IMAGE-BUFFERS-HEADER-AND-PAYLOAD-2813E` · Package: `_index/candidates/opus-save-image-buffers-header-and-payload-ee-1003/` · Page: `19-Save-Load-Settings/Save-Image-Layout-And-Pipeline/save-image-buffers-header-and-payload.md` (commit 81c16b70b)

## SWE2-AUDIT-SPEC verdict: ACCEPT-WITH-NARROWING

All 3 rows were read clause by clause against the bytes. Rows `007B9F80` and `0087AF40` are exact, and so are all 15 anchors. Row `007BA7E0` needs one clause replaced: it names the `.rdata` constant by its address where the bytes compare against the dword stored there, and it says "sums ... into" where the bytes add onto the existing dword (below).

## SWE2-AUDIT-SPEC checks

- `interior_applier.py` was re-run fresh without `--apply`. Output: `VERIFY 3 functions, 15 anchors`, `ALREADY`, `FAILS 0`, exit 0. `git status` on the page and the package was clean afterwards (HEAD b5028e7e9).
- `rows.json`: 3 rows, 15 anchors. Rejected 0, skipped 0, missing 0, corrections 2. Both corrections hold at the bytes.
- Semantic pass: **every row** was read against a full capstone listing of the certified image (SHA256 73461D08...). Extents come from `check_dispositions.load_functions`, and rip targets were resolved to their section.
  - `007B9F80` (208 B), exact.
    - A null `rcx` jumps to the epilogue (`007B9F8A`).
    - `al`=0 is stored to bytes `+0x16..+0x19` of `[rcx]`, which is re-read before each store (`007B9FA4`..`007B9FB6`).
    - The step is `edx`=byte; `rcx`=crc>>24; `rdx^=rcx`; `eax`=`[01CB5380+rdx*4]` ^ (crc<<8) (`007B9FE6`). The table is in `.rdata`, and crc starts at 0 (`r9d`).
    - Loop 1: the count is `movsxd [rcx+8]` with `jle` skip, and the loop runs on `cmp r10,r11` / `jl` (`007B9FEE`).
    - Loop 2: the count is `movsxd [r8+0x18]` over `[r8+0x10]`, with `jle` skip and `jl` (`007BA020`). Its index `r9` is still 0.
    - The little-endian store is `al`, `edx>>8`, `>>16`, `>>24` (`007BA02E`..`007BA048`).
  - `007BA7E0` (359 B). All clauses except the one replaced below are exact.
    - Remaining = `[+0xC]`-`movsxd [+0x10]`. The read position is `[+0]`+`[+0x10]`.
    - `test [+8],0x80000000` returns 0 (`007BA80B`).
    - `[+0x18]`==0 gates the header block. `cmp ebp,0x1b` / `jl` gives 0.
    - `cmp eax,[rip→01CB5780]` (`007BA835`): `01CB5780` is `.rdata` and holds the dword `4F 67 67 53`. A mismatch goes to the resync at `007BA8C3`.
    - `r9d`=byte`+0x1A`+27, and `jl` gives 0 (`007BA84C`). The loop adds bytes from `+0x1B` onto `edx`=`[+0x1C]` and stores it back (`007BA855`..`007BA875`). Then `[+0x18]`=`r9d` (`007BA877`).
    - `[+0x1C]`+`[+0x18]` > remaining (`jle`, signed) gives 0.
    - The dword `+0x16` is saved, zeroed, and the stack record {pos, hdr len, pos+hdr, body len} is passed to `007B9F80` (`007BA8B6`).
    - On a mismatch the dword is restored, then the qword `[+0x18]` is cleared and `memchr(pos+1, 0x4F, remaining-1)` is called through IAT `008C2A18` (`007BA8D6`). On null the end of data is `[+0]`+`movsxd [+0xC]`. Then `[+0x10]` = found-`[+0]`, and the function returns pos-found.
    - On a match, a non-null `rdx` record gets {ptr, dword len, ptr+len, dword body}. Then `[+0x10]` += page (`007BA924`), `[+0x14]`=0, the qword `[+0x18]`=0, and the page size is returned.
  - `0087AF40` (243 B), exact.
    - `edi`=`[rdx]`, then `[rdx]`=0 (`0087AF63`).
    - The stack record is at `rsp+0x20`, and its qwords `+0x30/+0x38/+0x40` are zeroed.
    - `0087C9F0(rec, [rsp+0xC0]` (5th arg)`, 01CC73A4` (`.rdata` "1.2.11")`, 0x58)` (`0087AF91`). A non-zero result is returned.
    - `+0x10`=`rcx` and `+0`=`r8` are stored after the call.
    - Refill: `+0x18` from `edi` and `+8` from `r9d`, each `cmova` with 0xFFFFFFFF (`0087AFBD`).
    - The flush is 4 unless `ebx`≠0 (`cmovne`). `0087BD60` (`0087AFE7`) loops while it returns 0.
    - Then `[r14]`=dword `+0x1C` and `0087C6C0(rec)` is called. The function returns `esi`, with 1 mapped to 0 (`0087B010`).

## SWE2-AUDIT-SPEC narrowings

`007BA7E0`. Replace

> resyncs if the dword at the read position differs from `01CB5780`, returns 0 if fewer than 27 plus byte `+0x1A` bytes remain, else sums the segment-table bytes into `+0x1C` and caches that header length in `+0x18`

with

> resyncs if the dword at the read position differs from the constant dword stored at `01CB5780` (`.rdata`, bytes `4F 67 67 53`), returns 0 if fewer than 27 plus byte `+0x1A` bytes remain, else adds the byte `+0x1A` segment-table bytes from read position `+0x1B` onto dword `+0x1C` and caches that header length in `+0x18`

Why: `cmp eax, dword ptr [rip+...]` compares against the dword stored at the address, not against the value 0x01CB5780. The sum loop also starts from the existing `[+0x1C]` (`007BA855 mov edx, [rdi+0x1c]`) rather than from 0. Within this body that dword is cleared together with `+0x18` on every path that clears `+0x18`, but its value on entry is not the body's to state.

Limits: these are body statements read from static evidence. The cloud draft and OPUS's re-read are not independent review; this record is.
