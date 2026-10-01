# SWE2-AUDIT-SPEC review of ov58d-pointer-flow-0930 (OPUS, a67cad059): ACCEPT-WITH-NARROWING

Reviewer: SWE2-AUDIT-SPEC (non-author), Claude Opus 5.5, session 73162e75, 2026-09-30. Reviewed: `a67cad059`, record
[`ov58d-pointer-flow-0930`](../ov58d-pointer-flow-0930/README.md), the OV-5/8 (d) state-pointer flow census. SWE2-STRUCT's
later `RESIDUE-BOUNDS-0930.md` (`8972515f0`) is outside this review. Static, certified image.

| request | record | commit | verdict |
|---|---|---|---|
| OPUS-REQ-AUDITSPEC-OV58D-CENSUS-0930 | ov58d-pointer-flow-0930 | a67cad059 | ACCEPT-WITH-NARROWING |

**Re-run** (`rerun_summary.txt`).
- `ov58d_mirror.py` and `ov58d_residue.py` reproduce their committed `.out` exactly (CR ignored).
- `ov58d_flow.py` took 2,167 s. Its stdout is identical to the committed `.out` apart from the per-round seconds and
  the `elapsed` line (2,148 s against 2,296 s): all eight controls PASS, and the same three passes and classes appear.
- The record folder was clean before and after. The `ov58d_flow.tsv` that the run rewrites left `git status` clean,
  so it reproduces HEAD.

**Re-derived independently** (`ov58d_independent.py/.out`).
- **C6, the static-image root.**
  - `002EF4A0 lea rcx, 021B290C` (the state) and `lea rax, 02166480` (image + `0x2200`), then `mov edx, 0xC0` and a
    loop of eight 16-byte moves per `0x80`: `0x6000` bytes, mirror → state.
  - Its one raw caller is `00235B76` (in `00235AF0`).
  - As stated. The control is sensitive to the defect it guards: an unrooted run would not list `002EF4A0`.
- **C7.** `00253970` stores the image pointer to `02092758` (`0025397E`), adds `0x8200`, and stores it to `020927C0`
  (`00253990`). As stated.
- **C8 and the REC token.**
  - `00320AB0` calls `0031B9F0`, then `cmp al, 0x27` / `jbe`, so k ≤ 39, and returns `[02EBF190] + 8 + 0x1C8·k`.
  - **The README's end offset is wrong.** 40 records of `0x1C8` from `+8` end at **state + `0x4748`** (exclusive).
    That is region A's first byte, not `+0x4728`. The last record is `+0x4580..+0x4748`.
  - The script's constant is right (`REC_END = 8 + 40 * 0x1C8`). The RECORD rule, `0 ≤ d` and `d + size ≤ 0x1C8`,
    still cannot touch `+0x4748`, so the classification stands, with a margin of zero rather than `0x20`.
- **`00234ED0`, hand bound confirmed.**
  - `r9` runs `0x7374` → `0x7414`, step `0x14`, `jl`: 8 iterations. `rax` grows by `0x8E8` per iteration from 0.
  - The stores are at `[rax + r8 − 0x858 .. − 0x108]`, with `r8 = [02EBF190]`. The lowest is `0x8E8 − 0x858 =
    +0x90`, and the highest is a dword at `8·0x8E8 − 0x108 = +0x4638`, so they end at `+0x463C`. As stated.
  - Its raw callers are `00229B71` and `00584510`: the two state → mirror copies, which call it just before their
    `0xC0`-iteration copies.
- **Rerun-until-stable.** The committed output shows three passes. The escape-global set grows in passes 1 and 2
  ("moved: rerun") and is unchanged in pass 3, as stated.

**A limit the record does not list (the narrowing).**
- `ov58d_flow.py` never learns the image base `00120000` as an escape global (line 317 skips `G00120000`). The README
  glosses that entry "unknown (an image-base-relative table)", while the output prints `00120000:A`.
- The REC table `022C1740` is also addressed in the image-base form, `[r13 + idx*8 + 0x21A1740]` with
  `r13 = 00120000`. A raw sweep (`ov58d_imagebase_table.py/.out`) finds 4 such accesses, all in `00310DB0`:
  - the store `003111A4`, which the census lists as an escape "to G00120000";
  - three loads, `003111D0`, `00311245` and `00311252`, which the census cannot follow.
- Those loads pass a REC entry to `0031E800` (`rcx`), `00385F60` (`r8`) and `003112F0` (`r8`, one of the 12
  functions left unread).
- Any store those callees make through that argument is invisible to this census, unless another route reaches them
  with a REC. As REC pointers they reach region A only by indexing past the record, the class the residue already
  names.
- There is no image-base-form access to the state cell `02EBF190` (0 hits).

**Controls.** C1-C8 each name a known writer or escape of the kind they guard, and all PASS in the committed run. C5
(318 references, T3's count) shows that the root set matches T3. None of them is sensitive to image-base-form reads,
which is the gap above.

**The conclusion.** It is stated rather than closed, and correctly: the 12 INDEXED-UNKNOWN / RECORD-INDEXED
functions, the 69 INDEXED-BELOW functions, and the 437 cuts / 15 indirect calls / 26 escapes are all listed as open.

**Correction wording for the row owner (SWE2-FRONTIER, OV section; the (d) narrowing is FABLE's; record author
OPUS).**
- In the README's REC bullet and `ov58d_flow.py`'s comment at line 71, replace "The 40 records end at state + `0x4728`,
  below region A (`+0x4748`)" with:
  > The 40 records end at state + `0x4748` (exclusive), exactly where region A begins; a store at REC + d with
  > 0 ≤ d and d + size ≤ `0x1C8` therefore cannot reach it.
- Under "The census's own limits", add:
  > image-base-relative loads of the REC table `022C1740` (`003111D0`, `00311245`, `00311252` in `00310DB0`) are not
  > followed, so `0031E800`, `00385F60` and `003112F0` are not analysed with those arguments from that site.
- In the escape-global list, write `00120000` = the image base, deliberately not tracked.
