# EXP-258 — `00422C20` `+0xC4`/`+0xC8` resolver arms (direct entry)

**Status:** complete — **560/560 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `316e49c0` prefix; 560
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn on a new direct-entry fixture; nothing claims
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..257).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Mechanism exercised (all shipped bytes, four new `d422c20-*` cases)

EXP-257 promoted `00422C20` with all three slot fields planted -1, so
the resolver arms were skipped. This package plants a mode-1 slot
container and runs both `0051BA40` arms for real.

- `d[elem+0x10]` is a **byte offset into the elements arena**
  (`0020E600(off) = q[01F83530] + off` — EXP-257's `0xBFFFF000` was
  the matching `0020E620` inverse `ecx - d[01F83530]`). The resolved
  element's `q[+0xDA8]` is the container.
- **`0051BA40(container, slot)`** — indexed detach: `0051F240`
  dispatches on `d[C+4]&3` (sign-extended 2-bit mode). Mode 1 →
  `desc = q[C+8] + slot*0x30`; `b[desc]&2`==0 → return `q[desc+0x18]`
  (a direct data pointer; &2 would resolve `q[desc+0x10]` via
  `003AB7F0`). `0051BA40` then `ebx = d[record]` (the release key),
  **`0041CF00(record)`** resets it (`w[R+0x28]`==0 → row loop skipped;
  `d[R+0xC]&0x1000`==0 → the `2ED570`/`372280` arm skipped; tail
  **`0041CB90`** performs the ~0x390-byte field reset — `d[R]`..`d[R+8]`
  =-1, `d[R+0x324]`=-1, `d[R+0x358]`=0x10, `-1.0f` at `+0x344..0x34C`,
  `f[01DFE0BC]*30.0` at `+0x340`), then **`0051F190(C, key)`** clears
  descriptor `A[key]` and decrements `d[C+0x14]` (→ `d[C+0x18]`=0 if
  it empties).
- **`0051F4C0(C, key)`** (inside `51F190`) — the w-index unlink:
  `d[C+0x10]`!=0 gates it; mode-1 → array `q[C+8]`; desc's
  `d[+8]`/`d[+0xC]` low-words are prev/next slot indices — linked
  neighbours get `d[prev*0x30+0xC]`/`d[next*0x30+8]` patched;
  container head `d[C+0x1C]`/tail `d[C+0x20]` equal to the released
  key adopt the desc's (here -1) links; `q[desc+8]`=-1.

## Cases

- **`d422c20-c4`** — slot 1 via `d[+0xC4]`: `d[+0xC4]`=-1 and
  `w[+0xCC]`=-1 written (only this arm writes `+0xCC`); record reset
  pinned; desc `A[key]` released; head fixup `d[C+0x1C]`: 2→-1; tail
  3 untouched; count 2→1. The popped desc's `q[+0x18]` link is NOT
  cleared (pinned — `51F240` only reads it).
- **`d422c20-c8`** — slot 0 via `d[+0xC8]`: `d[+0xC8]`=-1, `w[+0xCC]`
  sentinel `0x1234` **unchanged** (the arm writes no `+0xCC`), tail
  fixup fires (1→-1), head 0xFFFF untouched.
- **`d422c20-both`** — both arms on one container: two pops, two
  releases (`A[2]`, `A[3]`), head+tail fixups both fire, count 3→1.
- **`d422c20-mode2`** — `d[C+4]&3`==2 → `0051F240` ret 0 →
  `0051BA40` skips reset+release entirely (record still keyed,
  desc fields zero, count unmoved) — but `422C20` still retires
  `d[+0xC4]`=-1 / `w[+0xCC]`=-1. Container mode ≠ deregistration:
  the slot fields always clear.
- All four also pin the EXP-257 clear block running unchanged
  (`d[+0x69C]`=`0xBFFFF000`, `b[+0xC0]`&=0xBF) with the arms live.

## Not claimed

- `00422C20`'s `d[+0x18]` arm through `002ED570` (needs the
  `003AB7F0`-resolving `q[C+0x30]`/`q[C+8]` table pair and the
  `0x10`/`0x20`-stride row machinery), `0051BA40`'s mode-0
  (`003AB7F0` lookup) and `b[desc]&2` (indirect `+0x18` resolve)
  arms, `0041CF00`'s `w[R+0x28]` row loop and `d[R+0xC]&0x1000`
  arm (`2ED570`/`372280`), `003AB7F0` itself, `005369C0` real,
  `q[02EBF188]` consumers, live-game reachability —
  `NATIVE-REPLAY`, `live_game: false`.
- `b3b02a0` ×14 remains scripted: `003B02A0` needs a modelled engine
  heap — `36BC60`'s free-block descriptors carry `20E600`-resolved
  fields over `022D7FD0`-indexed heap rows; deferred with `5369C0`.
