# OV-31: type-store work for the title-asset widget (SWE2-STRUCT, 2026-09-29)

Board task `FRONTIER-REQ-SWE2-STRUCT-OV31-TYPE-STORE`. The type is `WidgetSingleton02AEE4C0`: the
`0xD8` asset widget whose pointer is in the cell `02AEE4C0`. The page is
[`the-title-asset-singleton-and-its-distinct-consumer.md`](../../../16-UI/Widget-Object-Model/the-title-asset-singleton-and-its-distinct-consumer.md),
section 8. Only the shipping image was used (sha256 `73461D08...`); no live game.

## Files

| File | What it is |
|---|---|
| `ov31_title_asset.py` | Re-runnable checks S, P, J, X, C, O and K, plus `--self-test` (about 3 minutes; `--quick` skips the census). |
| `apply_ov31.py` | The idempotent patch that wrote the `_types` rows, the page section and box, and the register row. `--check` is a dry run. |
| `unapply_reg_ov31.py` | Withdraws only this lane's OV-31 register cell from the worktree. It exists because `_index/OPEN-QUESTIONS.md` carried a peer's unpublished UQ-206 edit at publication time, so the register row and the page box could not be published yet. `apply_ov31.py` re-applies them. |
| `run.out`, `selftest.out` | The outputs of the run published with this record: every family PASS, and every self-test mutation fired. |

## What each check establishes

- **S.** 35 cited instructions decode to the exact recorded text. This covers every width claim:
  - the `+0xC0` DWORD writes and its BYTE/DWORD reads;
  - the `+0xC8`/`+0xD0` QWORD accesses;
  - the extent (`0039449F`);
  - the pool/heap branch (`00244F77`, `00244F90`, `00244FB2`);
  - the default stub (`005C5230`);
  - both release sites;
  - the `fsttl_initialize` poll;
  - the batch owner sites.
- **P.** Each cited site lies in the named `.pdata` chain root, never in the first fragment. For
  example, `0024505A` lies in `[0024502D,00245080)`, which chains to the root `00245020`. `00394500`
  and `002486B0` have no `.pdata` entry, because they are leaf functions. Their bodies were read
  whole, up to `ret` and the `int3` padding.
- **J.** In `00582860`'s jump table (`00582899`/`005828A0`, index = message - 1), message 18 goes to
  `00582E81`. That is the arm that calls `00394520`, then `00394400`.
- **X.** `data_xref_scan.py` finds exactly nine references to `02AEE4C0`. The scan matches both the
  RIP-relative and the image-base forms, and its control `02AEE4D0` passes. The nine sites are in
  `003939B0`, `00394070` (two), `00394130`, `00394400`, `00394460`, `00394500`, `00394520` and
  `00394530`.
- **C.** The cell-seeded `census_receiver_fixpoint` with the extent widened to `0x1000` reaches 13
  functions and converges. Its type-area sites are exactly `00393A98` (+C0, 1B, r), `0039450D`
  (+C0, 4B, r) and `00393AA5` (+D0, 8B, r). It finds nothing at `+0xC4`, nothing at or beyond `+0xD8`,
  and nothing at `+0xC8`. Every access below `+0xC0` is in common widget code on the `00244F00` chain.
- **O.** `SEED=ctor 00394070 ARGREGS=1` with the extent at `0x1000` reaches 4 functions and converges.
  It finds exactly the seven own-handler sites. Below `+0xC0` it finds only `00244960`
  (`+0x10`, the attach entry of the widget contract).
- **K. Positive control for the `+0xC4` zero.** The same tool on the sibling cell `02AEE4C8` reports
  `+0xC4` accesses at `0039435C`, `0039436A` and `003944E0`.

A raw sweep found the callers. It covered E8/E9 rel32, abs64 and rva32 in every section, with the
control that `00244F00` has 269 hits. Every hit was then read in its calling window:

- `00394400` has one call, `00582EB5`. The `rva32` hit at `0174D1D5` is an odd, unaligned address in
  `.rdata`, not a table entry.
- `00394520` has one call, `00582EAC`.
- `00394500` has one call, `00511EC4`.
- `00394460` is reached from `00511EAD` (jmp).
- `00394530` is reached from `00511FA3` (jmp).
- `00511EA0`, `00511EC0` and `00511F90` are verb-table slots (abs64 at `01F29EE8`, `01F29EF0` and
  `01F29F60`). These slots match the verb table's rows 7055 and 7058.

## Falsifiers stated and searched

- `+0xC0`: a write of any other bit or width, or a reader of another bit, on an enumerated path.
  None was found.
- `+0xC4`: any access. None was found, and control K passes.
- `+0xC8`: any access other than `00394033` or `00394097`. None was found.
- `+0xD0`: any access other than `00394050`, `003940A8`, `003940B9` or `00393AA5`. None was found.
- Extent `0xD8`: a type-specific access at or beyond `+0xD8` in a widened census. None was found.
- Header embedding: a type-specific body touching below `+0xC0`. None was found; only common widget
  code does.

## Residue (not smoothed)

1. `+0xC4` stays DISCOVERED/UNKNOWN, typed `u8[4]`. Accesses through the UI-root child link made at
   attach (`00248220`) are not excluded, because those generic walkers were not read one by one.
2. Release through a teardown of the parent root `*(0208EA28)` is not established.
3. Whether the asset takes the deferred branch is not established. That covers `00244DD0` and the
   `+0x40` bit `0x20` deferral, which `00248271` copies from the parent at attach time.
4. Real IO and callback timing is OV-29, and type readiness is OV-32. Readiness is left at SIGNATURE
   RESOLVED.

## Publication order (SWE2-STRUCT, 2026-09-29)

1. `dcdd159f0` published the `_types` rows and this record.
2. The second commit publishes page section 8. The page box still reads "NOT A QUESTION". The box
   annotation and the OV-31 register row flip together, in the commit that can stage
   `_index/OPEN-QUESTIONS.md` without a peer's line.
