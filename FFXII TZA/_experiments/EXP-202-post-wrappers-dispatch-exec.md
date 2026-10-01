# EXP-202 — type-0/type-1 post wrappers `003283D0`/`00328480` + live `0028FBE0` dispatch

**Status:** complete — **407/407 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`1a40a8377d79e3b9606c100769cb7ca14f35950620821ffb3dfdc7cc392078a0`), zero
unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..201; 394 inherited + 13 new `d3d0-*`/`d480-*` direct-entry cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

EXP-201 queued the two remaining display-post wrappers. They required no
promotion — `003283D0` was already REAL (`n283d0`) and `00328480` unmapped
(native-by-default) — so this package is **direct-entry coverage plus the
first observable `0028FBE0` dispatch**: the new `fbtab`/`ctrl` fixtures
populate `00296280`'s 4-entry scan table and the `q[0209BE80]`→`q[+0x10F78]`
controller chain, letting the subtype jump-table arms actually fire into the
scripted `00296E90`/`00297040` sinks (which is what makes the subtype byte
observable — in shipped state it only selects a style index that always
misses the `002DD7E0` table, see below).

## `003283D0(obj, num, r8, r9)` — type-0 number post

- `edi = (r8*2) | r9` — caller's style pair packed into an index base.
- `002FA3B0(q[obj+0x10])` distance gate (`d3d0-null`/`far`).
- Request: `q[+0] = q[obj+0x10]` (the sub-object), `d[+8] = abs(edx)`
  (`cdq; xor; sub` — `d3d0-neg` formats `42` from `0xFFFFFFD6`),
  `b[+0xC] = 0` (type 0), `b[+0xD]` = **subtype** byte.
- **Subtype index:** `b[0x1EED300 + (edi + off)*4]` — byte 0 of the dword
  entry (shipped: `02 04 01 03 06 08 05 07` for idx 0-7). `off = 4` iff
  `(rec==0 || b[rec+5]!=0) && 00263C20(q[obj+0x10]) != 3`; else `0`.
  `00263C20` here reads `b[subobj+0xE]&0xF` (rcx is the sub-object at that
  call site — `d3d0-c20` plants `sob={0xE:3}` → off 0; `d3d0-rec` plants a
  `b5==0` rec → `263C20` not even called).
- Dispatch arm proven per subtype (`fbtab` id 0 match + `ctrl` chain):
  subtype 2 → arm1 → `00296E90(ctrlsub, id)` (`d3d0-rec`/`c20`); subtype 6 →
  arm5 → `00296E90` (`d3d0-near`/`neg`); subtype 7 → arm6 →
  `00297040(ctrlsub, id, 1)` (`d3d0-sub`); subtype 1 → arm0 →
  `00297040(id, 0)` (`d3d0-arm0`); subtype 4 → arm3 no-op (`d3d0-arm3`);
  subtype 8 → `subtype-1 = 7 > 6` → dispatch skipped entirely
  (`d3d0-sub8`).

## `00328480(obj, edx)` — type-1 post

Same distance gate; request `{subobj, edx, type 1}` → `00506700` type-1 arm:
`b[+0x3F] = b[req+8]`, `0024A5A0("battle_4_p")` name (returns 0 under
shipped-static state — the `0208F580` string table's `&0x20` populated-flags
are runtime state), subtype byte pair `b[0xE02780 + b3f*2]`/`+1` → two
`002DD7E0` lookups → `d[+0xC]`/`d[+0x10]` (`d480-near`: `b3f=3` → indices
29/107, both miss the unplanted `dd7` table → `0x80808080`).

## `0028FBE0` dispatch path — now fully resolved

The EXP-201 note "subtype 0 falls through" is refined: `b[req+0xD]-1` bounds
a 7-entry jump table at `0x28FC8C`; only after `00296280`'s scan resolves
*and* `q[q[0209BE80]+0x10F78]` is non-null. `00296280` scans a fixed
`0209BFBE..0209C2BE`, 0xC0-stride table: entry live iff `b[e-0x58]&2` or
`b[e]&2`, match on `d[e+0x32] == packed-id`, returns `e-0x7E`. The packed id
is `003589B0(obj)` = `w[obj] | ((w[obj+0x16]&0x7FF | ...)<<20)` — a zeroed
sub-object packs to 0, which `d3d0-*` matches against `fbtab={0:{fl:2}}`.

## Corrections of record

- EXP-201 said "`bd00-t0` exercises scan+controller only (subtype 0 →
  `edx=-1` → `ja`)": confirmed, and now complemented — every arm is
  reachable and the `0x28FC8C` table maps `[0,4]→297040(0)`,
  `[1,5]→296E90`, `[2,6]→297040(1)`, `[3]→no-op`.
- Subtype byte provenance: not `edi` directly — `b[0x1EED300+idx*4]` table
  byte; the `+4` offset selects the second quad when the object's record
  is absent/inactive and its low nibble class ≠ 3.
- `002DD7E0`/`002DD7B0` miss-path values confirmed live: `0x80808080` / `0`
  (the type-0 style indexes at `0xE027A8+sub*4` ship as large dwords —
  e.g. subtype 6 → `0x4F2B039D` — always missing a populated table).
- `d4d0-*`/`d3d0-*`/`d480-*` all share one fixture vocabulary; `n283d0` was
  already real — this package adds the entry coverage and the dispatch
  evidence, not new promotions.

## Validation

`python check.py` — 407/407, three independent runs, `result.json` SHA256
`1a40a8377d79e3b9606c100769cb7ca14f35950620821ffb3dfdc7cc392078a0`
identical each time. New fixtures: `dobjrec` (`q[dobj+0x698]` rec for the
subtype-offset gate), `sob` (extra `subobj` byte writes — `b[+0xE]` class
nibble), `ctrl` (`q[0209BE80]` controller + `+0x10F78` handler),
`fbtab` (`00296280` scan entries). `r8`/`r9` case keys already existed.

**Not claimed:** live-game reachability. `00296E90`/`00297040` remain
scripted sinks — their bodies are the consumer side and are the natural
next promotion. `0031C5D0`/`002B3050` remain scripted for the same reason.

## Receipt (SWE2-ORACLE, 2026-09-30)

- **This record's run is sealed receipt `r-edb8403635767456`** (`_experiments/evidence/receipts/store/`). The shared
  `member-block-chain-exec/result.json` has moved on since. Cite the receipt, not the path.
- **Regression:** `_experiments/evidence/receipts/exp201_receipts.py check` (receipt `R-EXP-202-*` rows). Precision
  point 2 of `AUDITSPEC-REQ-ORACLE-EXP201-PRECISIONS-0929`.
