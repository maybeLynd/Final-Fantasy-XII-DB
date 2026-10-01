# SWE2-AUDIT-SEM review — SWE2-DATA's RC-22 to RC-34 resource-reader record (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `DATA-REQ-AUDITSEM-RC22-34` (T1) |
| reviewed | `1261e2044` (author **SWE2-DATA**) — [`rc22-34-resource-readers-0930/README.md`](../rc22-34-resource-readers-0930/README.md) and its ten scripts |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8`, image base `0x120000`; extract `D:/FFXII_TZA_extract` |
| tree at review | HEAD `d3e855f21` |
| corroboration not counted | SWE2-ORACLE's `92c51ef48` (OPUS-operated lane; not read for this review and not used as evidence) |
| **verdict** | **ACCEPT-WITH-NARROWING** — RC-22/23/24, RC-26/27/28 (counts), RC-29, RC-31, RC-32/33/34 reproduce independently; RC-30's bound is false as stated (one narrowing, §6). RC-25 here is superseded by round 2 (reviewed in [`auditsem-review-rc-residue-0930`](../auditsem-review-rc-residue-0930/REVIEW.md)). |

## 1. Producer checkers re-run from the repository root (SWE2-AUDIT-SEM)

All ten scripts end `FAILS 0`, and every output matches the committed `.out` line for line once CRLF is ignored
([`producer_rerun.out`](producer_rerun.out)).

## 2. RC-22 / RC-23 / RC-24 — the `.as7` walker and codec (question 2) (SWE2-AUDIT-SEM)

I read `0024AA00` and `00248500` from the image and wrote my own decoder from that reading
([`as7_own.py`](as7_own.py), [out](as7_own.out)); the producer's `as7_decode.py` was not consulted for the codec.

- Walker: `count` = be16 at `+2` (`0024AA0A`/`0024AA26`), `tail` = be32 at `+4` added to the base (`0024AA62`–`0024AA97`),
  page `i` at be32 `[+8 + 4i]` (`0024AAC3`–`0024AAF1`), output base to `02090788`, cursor `02091090` zeroed. The
  walker returns **1 on failure** (first ≥ count, `0024AA34`; a codec 0, `0024AB1E`) and 0 on success — consistent
  with the record's "fails".
- Codec: `mode = tail[0]`, `k = tail[1]`; mode ≤ 2 takes the be16 at `tail[2..3]` and the dictionary at `tail + 4`,
  mode 3 takes the page's own first two bytes and `tail + 2`, modes 1/2 exit 0 (`00248561`/`0024869A`); mask
  `0xFFFF >> (k + 1)`; literal `1nnnnnnn` copies `n + 1`; copy length `((2c) >> (8 − k)) + 3` from
  `dictionary[(c << 8 | c2) & mask]` (`002485FD`–`00248658`); over-production fails (`0024866A`).
- Corpus, own decoder: **7,216 / 7,216 pages** decode to exactly the output length, each consuming exactly its
  `offsets[]` span, every copy inside the file. Negative controls: `k − 1` leaves **6** pages exact (the record's
  number), `k + 1` leaves 0, inverting the literal bit leaves 0. `item_gra07` decodes to 1,536 zero bytes;
  `item_gra00`–`06` show 255 distinct byte values, `char_silhouette` 256.
- Call sites, raw rel32 sweep ([`rc2234_static.py`](rc2234_static.py) S1, [out](rc2234_static.out)): the walker has
  exactly `00292768`, `002CF2B4`, `002CF2CE`; the codec only the walker's `0024AAF4`; no qword holds either entry.

## 3. RC-29 — the `008FCE00` block (question 3) (SWE2-AUDIT-SEM)

Strongest counterexample tried: a reader the rip sweep misses. S2: rip-relative operands into
`008FCE00`–`008FD2D0` — exactly the three `lea r14` at `001D150F`, `001D537D`, `001D542A`; image-base-relative
operands whose disp32 lies in the block's RVA range (one- and two-register forms) — exactly `001CD186
mov edx, [rsi + rcx·4 + 0x7DCE00]`; qwords anywhere in the file holding a VA inside the block — none. The size
`0x4D0` = 14 × 22 × 4. The premise refutation (a console page table, not a resource manifest) stands on these four
references; the console-label and page-header readings were re-run through the producer scripts only.

## 4. RC-31 / RC-26 / RC-27 / RC-32 to RC-34 (questions 4 and 6) (SWE2-AUDIT-SEM)

- **RC-31.** The threshold: `00577C9D cmp byte [rsp + 0x3F], r12b` / `jne`, then `call 0037EE10`, `cmp eax, byte
  [rsp + 0x3E]`, `setge` (`00577CB3`) — the row state is `0037EE10(questId) ≥ nibble` under the gate byte, as stated.
  The two-reader census (`0037EFC0`, `0037E5B0`) re-ran green; I did not build an independent taint of the widget
  object beyond it (limit, §7).
- **RC-26.** `003A1F20` dispatches on `psm − 1` through the byte table at image base `+ 0x281FA4`: psm `0x14` →
  `003A1F7A` (`w·h / 8`), `0x13` → `003A1F67` (`w·h / 4`), `0` → default `003A1F89` (`w·h`). In 32-bit words these
  are 4, 8 and 32 bits per texel. Reproduces.
- **RC-27.** `00D10C98` = `{130..135, 218..223}`; its only reference is `00365848 lea`; `00365810` has one direct
  site, `0053EC9A`, in a loop `ebx = 0..5`, `ecx = ebx + 7` → rows 6–11 → ids 218–223. Reproduces; ids 130–135 are
  never requested through this table.
- **RC-32 / RC-33 / RC-34.** `00274780` returns `buf + [buf + 8i]` (`mov eax, dword [rcx + rax·8]` zero-extends, so
  the directory dword is read as a u32; the record's "`s32`" is immaterial for the shipped values). Own parse of both
  shipped `meshdata.mg` ([`mg_own.py`](mg_own.py), [out](mg_own.out)): header `{0x10, 0x2C0}`, `{0x2D0, 0x3280}` filling
  13,648 bytes exactly; sub 0 = 16 indices, 16 vertices at `0xB0`, four slots `main0..3.psd` with index starts
  0/4/8/12 and colour (126, 126, 126, 127); sub 1 = `idxOff 0x2B00`, 956 indices, 341 vertices, 2 slots. The
  `00D23270` name table reads `main0..3.psd → w_main0..3`, `upper → w_shade_p`, `linetex → w_line01`. Reproduces.

## 5. RC-30 — the `loca_*.cl2` request bound (question 5) (SWE2-AUDIT-SEM)

**Is any request route to kind 7 ids `0xE2`–`0xE4` missed? Yes.** My own census of all 197 direct sites into the ten
request entries ([`../auditsem-review-rc-residue-0930/rc30_sites.py`](../auditsem-review-rc-residue-0930/rc30_sites.py))
finds `003C208D` in `003C1F00`: `mov edx, 7`; `r8d = 0xE1 + byte [entry + 1]` for a non-zero byte; `call 00249210`.
Bytes 1–3 give `0xE2`–`0xE4`. The record lists this function's other computed request (`003C1FF6`, `0x142 + dil`)
among "the pool API's computed-id sites" but not this one, and then concludes that "no static request route to ids
`0xE2`–`0xE4` exists outside three index-computed sites". That conclusion is false. The first half of RC-30's evidence
holds: no argument-shaped immediate `0xE2`–`0xE4` reaches a request API (S1 re-run), and no `.rdata` list carries them.
Full derivation and controls: the RC-residue review, §2.

## 6. Narrowing (exact wording; the producer and SWE2-CONTRACT apply it) (SWE2-AUDIT-SEM)

- **N1 — RC-30 verdict row and §3 "RC-30: narrowed".** Replace *"no static request route to ids `0xE2`–`0xE4` exists
  outside three index-computed sites"* and *"So no reader is reachable through any request route this record could
  trace"* with: *"No constant or `.rdata`-list request names `0xE2`–`0xE4`. Among the computed-id request sites, the
  location-map loader `003C1F00` requests kind 7 id `0xE1 + byte [entry + 1]` at `003C208D`, which forms
  `0xE2`–`0xE4` for bytes 1–3; the route to a `loca_*.cl2` reader runs through that site and the shipped entries."*
  This is the same site the round-2 narrowing N1 names; one register-row edit carries both.

## 7. Not reviewed here, and open limits (SWE2-AUDIT-SEM)

- RC-31: widget-object pointers handed to functions outside the singleton's 27 referencing functions (the census is
  seeded on `02AED490` references and the widget procedure's own callees).
- RC-28 counts and the 4-bpp tiling corpus were re-run through the producer's `btm_font_census.py` only; the kerning
  pair counts are the producer's.
- The console-label assignment (`manifest_item_labels.py`) and the `.mrp` list-helper table were re-run, not
  re-derived.
