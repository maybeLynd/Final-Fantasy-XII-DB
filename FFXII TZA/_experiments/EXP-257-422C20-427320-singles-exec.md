# EXP-257 — `00422C20` dereg + `00427320` edi-switch promoted real

**Status:** complete — **556/556 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 `4499a6ef` prefix; 556
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn on the extended `u43f0-ec` fixture; nothing
claims initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..256).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Mechanism exercised (all shipped bytes, `u43f0-ec` only)

Both remaining singles fire exactly once on `u43f0-ec` (rcx=elem2 =
`w.ecarr + 2*0x740`); the two scripted boundaries `v422c20` and
`v427320` are retired.

- **`00422C20` — ecarr-row deregistration + clear block.** Three slot
  fields each gate a resolver arm: `d[obj+0xC4]`/`d[obj+0xC8]` !=
  -1 → `0020E600(d[obj+0x10])` → `q[rax+0xDA8]` → `0051BA40(list,
  slot)` then `d[slot]`=-1 (slot 0 also `w[+0xCC]`=-1);
  `d[obj+0x18]` != -1 → `0020E600` → `q[rax+0xD98]` →
  `002ED570(list, slot)` → `d[node] &= ~8`. All three fields planted
  -1 → arms skipped; the **clear block runs**: `q[+0x68]`, `q[+0xD8]`,
  `q[+0xE0]`, `q[+0xF0]`, `q[+0xF8]` = 0, `d[+0x23C]` = 0,
  `b[+0xC0] &= 0xBF`, and `d[+0x69C]` = `0020E620(0)` **twice**
  (second call's eax lands last).
- **`00427320` — edi-class applier.** Head: `003E55F0(rbx)` →
  `rsi = q[rbx+0x400]`; `003E7D10(d[rbx+0x6A4], 3)` — row 0 of the
  `02B59D80` table is empty on the fixture → ret 0 → jumps past the
  `edi & 0xF000`/`edi-0x2007`/`bt 0xA3` gate chain to `004273A2`.
  `edi=0x1001` matches neither `0x2005` nor `0x2006` → `004274B6`
  tail: `d[rbx+0x284] & 0x8000000` clear → `00420890(rbx, edi)` —
  `edx+0xFFFFDFFB` = `0xEFFC` > `0x37` → default case →
  `002ED500(q[rbx+0x108]=0, 0x100, &stk)` → null arm zeroes the 0x40
  out-buffer → `d[rbx+0x110] = (d[stk+0x30] & 0x50)` = 0 → cookie,
  ret. Then `00423790(rbx, edi, w[rbx+0x3B4]=0)`: `d[rbx+0xC4]`==-1
  → skips `0051B9E0` → eax=0 → `w[+0x3B4]`==0 → `test rax` →
  **ret 1** → `00427320`'s `cmp eax,1` passes → class dispatch
  `d[0x427844 + ((edi>>0xC)&0xF)*4]` → **class 1**: `0020E600`×2
  (`e600` tags at trace 48–49) + `d[elem2+0x294] |= 8` — pinned via
  the downstream fold total (`0x401084` → `0x40108C`) since the bit
  lands *before* `2EB0D0`'s `4278B0`/`427860`/`4272A0` folds.

## Corrections of record

- `0020E620(ecx)` returns `ecx - d[01F83530]` — a **nonzero** BSS
  base counter (`0x40001000`), so `d[elem2+0x69C]` lands
  `0xBFFFF000`, not 0. Pin asserted to the shipped value.
- `00423790`'s `d[+0xC4]`==-1 early path returns **1**, not 0 — the
  `00427320` class switch therefore dispatches (class 1) rather than
  falling to the epilogue. The `d294` pin gained the `|=8` the
  switch arm contributes upstream of the folds.

## Not claimed

- `00422C20`'s resolver arms (`0051BA40`/`002ED570` — `51F240`
  derefs `rcx+4`, so a null list head faults; the arms need planted
  `q[elem+0xDA8]`/`+0xD98` list heads), `00427320`'s `0x2005`/`0x2006`
  arms and the `edi-0x2007` `bt` gated arms, `00423790`'s nonnull-row
  path (`0051B9E0` + signature map), `005369C0` real,
  `q[02EBF188]` consumers, live-game reachability —
  `NATIVE-REPLAY`, `live_game: false`.
- Remaining stub census unchanged apart from `v422c20`/`v427320`.
