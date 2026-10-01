# EXP-204 — `00273320` id→slot-index resolver + table leaves, executed

**Status:** complete — **424/424 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`fecb4789481a5198988fba27a6374ef61c2652e7db8931ab08a006b702d88b75`), zero
unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..203; 418 inherited + 6 new `r3320-*` cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

EXP-203 left `00273320` as the last scripted edge inside the `0028FBE0`
dispatch consumers. It is a small scan over a `0xC0`-stride table — this
package promotes it and its two leaf callees (`0035BB00`, `0035BB60`) to
executed bodies. With this, the entire post path — wrappers `003283D0`/
`00328480`/`003284D0` → `002FA3B0` gate → `003BBD00` ring → `00506700`
init → `0028FBE0` subtype dispatch → `00296E90`/`00297040` sinks →
`00273320` resolve — runs native end-to-end under fixtures.

## `00273320(id)` — first-match index scan

- `id == 0` → `0xFFFFFFFF` immediately, no count read (`r3320-nul`).
- `n = 0035BB60()` = `movsx eax, word [022C8064]` — **signed word**;
  `n <= 0` → `-1` with zero probes (`r3320-empty`, `r3320-neg` where
  `n = 0xFFFF`).
- Loop `i = 0..n-1`: `0035BB00(i)` = `d[022C8084 + i*0xC0]`; first entry
  equal to `id` → return `i` (`r3320-hit`, `r3320-hit2`); full miss → `-1`
  (`r3320-miss`). The count is **re-read after every probe** — the loop
  bound is live, not latched (verified by instruction order; `l35bb60`
  appears `n+1` times on a full miss).

`0035BB00(idx)`: `movsxd idx; rcx = idx*3 << 6` (= `idx*0xC0`);
`eax = d[022C8084 + rcx]` — the dword at entry+0 is the match key.
`0035BB60()`: `movsx eax, word [022C8064]` — count cell.

Both cells live in the writable BSS window (`022C8xxx`) and ship zero —
so in shipped-static state the resolver returns `-1` and the sinks'
writes would be suppressed; the `t3320` fixture is what raises it.

## End-to-end consequence for EXP-202/203 cases

The dispatch cases now plant a *real* nonzero packed id — `sob` gives
`subobj` `w[+0] = 0x1234`, so `003589B0` produces `0x1234`, `00296280`
matches `fbtab` `id:0x1234`, and `00273320` resolves via
`t3320 = {n:1, ids:{0:0x1234}}` — slot 0 → `ctrlsub` flag writes as
before. `s273320_ret` is gone; miss paths (`e690-bad`/`p7040-bad`) are
now genuine table misses (`ids={0:0x999}` vs `id 7`).

## Corrections of record

- RIP-relative slip: the count cell is `w[022C8064]` and the table base
  `022C8084` — my first transcription read `0x2282064`/`0x2282084`
  (dropped digit on `0x35BB67 + 0x1F6C4FD`). The failed run showed
  `l35bb60` firing once with no probes — the live probe pinpointed the
  real cells.
- EXP-201/203's "id→slot resolver" was described as an opaque scripted
  scan; it is specifically a `0xC0`-stride dword-key table with a
  re-read signed-word count, distinct from `00296280`'s own `0xC0`
  table (`0209BFBE`, different VA and flag/key layout).

## Validation

`python check.py` — 424/424, three independent runs, `result.json` SHA256
`fecb4789481a5198988fba27a6374ef61c2652e7db8931ab08a006b702d88b75`
identical each time. New fixture: `t3320` (`{"n","ids"}`). `s273320`/
`s273320_ret` removed from SCR; `0x273320`/`0x35BB00`/`0x35BB60` REAL.

**Not claimed:** live-game reachability. `0031C5D0` (resource resolver)
and `002B3050` (string copy) remain the scripted boundaries on the
display path — both now sit on the *type-2* arm, which is the natural
next package.
