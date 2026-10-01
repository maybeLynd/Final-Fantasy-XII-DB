# SWE2-AUDIT-SEM review — SWE2-DATA round 2: RC-25 / RC-28 / RC-30 residue and the bucket-members narrowing (2026-09-30)

*SWE2-AUDIT-SEM (independent semantic auditor). OPUS's Claude subagent ran this lane on 2026-09-30.*

| | |
|---|---|
| request | `DATA-REQ-AUDITSEM-RC-RESIDUE-0930` (T1) |
| reviewed | `39d08c02f` (author **SWE2-DATA**) — [`rc-residue-0930/README.md`](../rc-residue-0930/README.md) and [`bucket-members-narrowing-0930/README.md`](../bucket-members-narrowing-0930/README.md), as committed (the uncommitted working-tree edit of the rc-residue README is not the reviewed text) |
| image | `FFXII_TZA.exe` SHA-256 `73461d08…d89721f8`, image base `0x120000` |
| tree at review | HEAD `d3e855f21` |
| **verdict** | **ACCEPT-WITH-NARROWING** — RC-28 (all three leftovers), the RC-29 side result, the bucket narrowing and the RC-25 domain stand; the RC-30 section's completeness claim is false (a missed kind-7 site forms `0xE2`–`0xE4`) and RC-25's writer claim is narrower than its conclusion. Exact sentences in §6. |

## 1. Producer checkers re-run from the repository root (SWE2-AUDIT-SEM)

All seven scripts at the reviewed commit (unchanged at HEAD) end `FAILS 0` ([`producer_rerun.out`](producer_rerun.out)).
Six outputs are byte-identical to the committed `.out`; `rc28_staffroll_faces` differs only in the print order of two
Python dicts (same keys and values), which is cosmetic.

## 2. RC-30 — the computed-id bound (question 3) (SWE2-AUDIT-SEM)

**Own census, no producer helper** ([`rc30_sites.py`](rc30_sites.py), [out](rc30_sites.out)). A raw sweep of `.text`
for every rel32 `E8`/`E9`/`0F 8x` whose target is one of the ten request entries (the pool API `00249180`,
`00249210`, `002493D0`, `00249350`, `00249320`, `00249380`, with kind in `edx` and id in `r8d`; the path API
`0032E400`, `0032E620`, `002DF980`, `002DF880`, with kind in `ecx` and id in `edx` — each verified by disassembly)
finds **197 sites**. No qword in the image holds any of the ten entries and no rip-relative operand names them, so
there is no indirect route to add. For each site the last writer of the kind and id registers is read, folding the
compiler idiom `mov edx, 7` / `lea r8d, [rdx + k]` into a constant.

- Controls: P1 the `Loca.mrp` request `00404107` classifies as constant `0xBF`; P2 DATA's own `0x142 + byte` site
  (`003C1FF6`) is found; N1 a non-entry target yields no site.
- Kind-7 sites whose id is `base + index` with `base ≤ 0xE4` and that are **not** in either committed list
  (`1261e2044` `cl2_requests.py` S2, `39d08c02f` §2 A/B/C): four.
  - `00291D04` (`0x98 + ebx`, `ebx` 0..9 → `0x98`–`0xA1`), `002C900B` (`0x74 + edi`, `edi` 0..1),
    `0056301F` (`0xAA + ebx`, `ebx` 0..7 → at most `0xB1`): bounded below `0xE2` by their loop exits.
  - **`003C208D` in `003C1F00`: `mov edx, 7` (`003C2071`), `movzx r8d, al` with `al = byte [entry + 1]` tested
    non-zero (`003C2068`–`003C206F`), `add r8d, 0xE1` (`003C207A`), `call 00249210`.** For `al` = 1, 2, 3 this
    requests kind 7 ids `0xE2`, `0xE3`, `0xE4`, the three `loca_*.cl2`. It sits in the **same function** as the
    `0x142 + dil` site both records list (`003C1FF6`), 0x97 bytes later.

**So §2's heading ("the index-computed sites cannot produce `0xE2`–`0xE4`") and the first record's RC-30 verdict
("no static request route to ids `0xE2`–`0xE4` exists outside three index-computed sites") are false.** The list they
bound was not the census of the computed-id sites; it missed a constant-kind-7 site whose byte index reaches the loca
ids with no bound in the code. This is the site SWE2-ORACLE reported (unpublished, `rc30-cl2-request-bounds-0930/`);
it is re-found here by my own sweep, not taken from ORACLE. Whether a shipped `menumap_common` entry carries `1`–`3`
at `+1` is a data question this review did not settle; it is not needed for the verdict, because the reviewed claim
is the absence of a route, and a route exists.

Side observation (shipped data, no code claim): the file-size tables give `loca_gil` and `loca_bhm` 2,112 bytes and
`loca_rbl` (`0xE4`) `-1` in US / FR / KR / CN; by §3(2)'s own reading of `002DF780` a request for `0xE4` is refused
before any path is resolved.

**Sites A / B / C.** The producer's arithmetic reproduces. Strongest counterexample tried on A: W1-style censuses
count byte stores only, so I swept every store of **any width** covering `+0xB2D`
([`cover_sweep.py`](cover_sweep.py) `B2D`, [out](cover_B2D.out)). Besides the two named byte writes there are nine
wider stores (`00186DD6`, `001D041F`, `001D042C`, `002969E5`, `0048AF4C`, `004B95D3`, `0070A822`). Two traced: the
setter `002969E0`'s receiver is `[[0209BE80] + 0x10F78]` via `0028F800` (all four callers), and `001D041F` is the
developer-console label filler — neither is `[0209AC30]`. The other five were not type-traced. That is the same
limit B already states for its 18 other `+0xC1` writers, so A's bound carries it too (§6 N2).

## 3. RC-25 — the silhouette index domain (question 2) (SWE2-AUDIT-SEM)

The chain P1–P5 and the script census S1 reproduce. The request asked me to test **"`0023AD8E` is the only writer
of a party page's `+4`"**.

- **Wide stores through `02EBF190`** ([`rc25_blockcopy.py`](rc25_blockcopy.py), [out](rc25_blockcopy.out)): W1
  accepts `byte`/`word` stores only. Tracking all 318 references at any width, 15 stores are flagged as covering a
  `+4`: 13 are `or dword [block + 4], imm/reg` into the block's header dword (e.g. `002399FB`, `00300B5A`,
  `00311BD7`), which lies before the first page at `+8`; 2 are 16-byte copies through `r15` / `r14` =
  `block + 0x5A48 + 0x12` / `+ 0x24` (`00326717`, `0032673E`), past the last page (`8 + 0x28 × 0x1C8 = 0x4748`).
  None covers a page's `+4`.
- **Callees handed a block-derived `rcx`** ([`rc25_callees.py`](rc25_callees.py), [out](rc25_callees.out)): 16
  callees, `.pdata` chain fragments followed; none stores over `rcx + 4`/`+5`. Positive control: the same code run on
  `0023AC80` reports `0023AD8E`.
- **The blind class: the block is static and has a mirror** ([`rc25_mirror.py`](rc25_mirror.py),
  [out](rc25_mirror.out)). `00233C25 call 002EF640` returns `02164280`; `00233C2A add rax, 0x4E68C` makes
  `*(02EBF190) = 021B290C`. **`002EF4A0` copies `0xC0 × 0x80 = 0x6000` bytes from `02166480` (`02164280 + 0x2200`)
  over `021B290C`** — every one of the 40 pages, so every page's byte `+4`. Its only caller is `00235AF0`, which
  compares the mirror's header dwords, `+0x5B42` and `+0x5B12` with the live block and copies when they differ. The
  copy uses rip-relative addresses, not `02EBF190`, so a census seeded on `02EBF190` cannot see it.

**So `0023AD8E` is not the only writer of a page's `+4`.** After `00235AF0` runs, a page's `+4` is whatever the
mirror holds. The domain `0`–`0x27` / `0xFFFF` survives if the mirror's pages were themselves produced from a block
that `0023AD8E` wrote (a save image of the live block is the obvious reading). No rip-relative instruction stores into
the mirror's page range (one 16-byte store at mirror `+0x317F` lands in page 27's `+0x15F`). Following `002EF640`'s
40 call sites (`../auditsem-review-takebacks2-0930/mirror_writers.out`) finds three mirror writers: the snapshot copy
`00229B76` from the live block (which keeps the proviso true in-process), the save-load copy `00866A4D`, and
`00583C00` from an external buffer `[[02CA99B8] + 0x588]` whose source is not traced. The
main-character result (`0`–`5` from `addpartymember`) is untouched: it is a script census, not a writer census.

## 4. RC-28 — the three leftovers (question 4) (SWE2-AUDIT-SEM)

- **(1) Language arms.** The jump table at image base `+ 0x1C04B0` reads back to the 11 arm addresses the producer
  prints, and lang 9 and 10 share the default arm `002DFF32`. Reproduces.
- **(2) KR / CN `.btm`.** Read directly: `FileSizeTable_KR` / `_CN` hold `-1` for kind 7 ids `0xDA`–`0xDF`, US / FR
  hold 42,240 / 29,184 / 32,256. `002DF780` indexes `kind · 0x1388 + id` (`0x1388` = 5,000) and `002DF7B0 cmp …, -1`
  / `002DF7B9 je 002DF85D` returns 0. Reproduces. The completion side stays open, as the record says.
- **(3) Accented glyphs.** Own parse of the `us` decompile, no producer evaluator ([`rc28_roll.py`](rc28_roll.py),
  [out](rc28_roll.out)): 688 `fsroll_nameA/B/C` calls; 527 literal, 161 of the form `(K + regI0)` inside a `for`
  loop with constant bounds, every one parsed. **638 distinct name ids** (the producer's number, re-derived); literal
  maximum 1,023, loop maximum 658; **none in 894–944.** Independently of the row decoder, a raw UTF-16LE scan of every
  shipped `menu03.bin` / `menu04.bin` ([`rc28_rawscan.py`](rc28_rawscan.py), [out](rc28_rawscan.out)) finds Latin-1
  accented units only in the `fr` / `de` / `it` / `es` `menu04.bin` (18 each, `Á á è é í ñ ó ö ú`, 4 × 18 = 72 as the
  record states) and none in any `menu03.bin` — so the roles, drawn with face B, carry none either. RC-28(3) stands.

## 5. The bucket narrowing and N3 (question 5) (SWE2-AUDIT-SEM)

N1 and N2 are applied **verbatim** from my record (`auditsem-review-bucket-members-0930/REVIEW.md` §6) in both sheet
rows, and `logicpack` gained the end slot as N2 suggested. `endslot_check.py` re-runs `FAILS 0` on six copies with the
end-slot and one-byte-truncation controls. **Stating N3 in the new record instead of editing the old one is
acceptable**: the old README is a correction record whose declared scope re-arms the correction gate on any edit, the
new record names the old bullet as dated history, and the in-place edit is routed on the board
(`DATA-REQ-FRONTIER-N3-OVERRIDE-0930`). Until that lands, the old bullet is PENDING PROPAGATION, not repaired.

## 6. Narrowings (exact wording; the producer and the incorporation owner apply them) (SWE2-AUDIT-SEM)

- **N1 — RC-30 (rc-residue §2 heading and the `OPEN-QUESTIONS.md` RC-30 row; also the first record's RC-30 verdict).**
  Replace "the index-computed sites cannot produce `0xE2`–`0xE4`" and "no static request route … exists outside three
  index-computed sites" with: *"Sites `002CEAE0`, `003C9950` and `00575C30` cannot form `0xE2`–`0xE4`. A fourth
  computed site, `003C208D` in the location-map loader `003C1F00`, requests kind 7 id `0xE1 + byte [entry + 1]` for a
  non-zero byte, so it forms `0xE2`–`0xE4` for bytes 1–3; the RC-30 route question turns on the shipped entries' `+1`
  bytes and on that site's consumer, not on the computed-kind structures alone."* The RC-30 row's residue sentence
  ("whether a shipped instance of those structures holds kind 7 …") is incomplete as the only residue. SWE2-DATA's
  uncommitted `rc30-census-0930` states this correction; when it is published it needs its own review.
- **N2 — RC-30 site A.** "exactly two byte writes at `+0xB2D`" is exact; add *"nine wider stores image-wide also
  cover `+0xB2D`; two write other objects (`002969E0`'s receiver `[[0209BE80] + 0x10F78]`, the console filler
  `001D0390`), five are not type-traced"*, matching B's stated limit.
- **N3 — RC-25.** Replace "`0023AD8E` … no other byte or word write" as the writer premise with: *"`0023AD8E` is the
  only byte/word writer of a page's `+4` among code that reaches the block through `02EBF190`. The block is static
  (`021B290C` = `02164280 + 0x4E68C`) and `002EF4A0` (called only from `00235AF0`) overwrites all 40 pages from the
  mirror `02166480`; a page's `+4` therefore also takes the mirror's value (mirror writers: the live-block snapshot `00229B76`, the save-load copy `00866A4D`, and `00583C00` from an untraced external buffer)."* The
  domain sentence then reads *"… `0`–`0x27` or `0xFFFF`, provided the mirror carries pages written by the same
  initialiser."* The RC-25 row's ANSWERED status holds for the six main rows (a script census); the domain clause
  carries the proviso.

## 7. Not reviewed here, and open limits (SWE2-AUDIT-SEM)

- The shipped `menumap_common` bytes that decide whether `003C208D` requests `0xE2`/`0xE3` in play, and the reader of
  that request (`003C26C0` per SWE2-DATA's uncommitted census).
- The source of `00583C00`'s buffer, one of the three writers of the party-block mirror `02166480`.
- The five untraced wide stores covering `+0xB2D`; the 18 other `+0xC1` writers (B's own limit).
- Wrapper-level request routes: my census enumerates direct sites into the ten entries; callers of pass-through wrappers
  (`00332250`, `0024AB90`, `00379A10`, the actor-resource loaders) are the D group the record already leaves open.
