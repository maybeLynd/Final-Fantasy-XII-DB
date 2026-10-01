# EXP-180 — `379760` extra-record allocator, `37AD10` cfg table, `3AC920`, `17D490`/`1D50D0`

Evidence class: NATIVE-REPLAY (deterministic Unicorn fixtures on the exact
shipping EXE, SHA256 73461D08…97f8). `17D490`/`3AC920` scripted only where
called as boundaries; `t17d490` runs `1D50D0` real via planted singleton.

Harness: `Temp\exp166_check.py` — **229/229, stable ×3**
(three independent processes).

## `379760()` — the `0x2ADD11C` extra-record allocator

The `379630` builder tail. Builds a 0x50-byte template on stack:

- `37AD10(0, &out)` → cfg row ptr (real, see below); `265920()`
  invoked (ret unused — side-effect/vestigial call).
- If row non-null: quad = `{f[row]*C1, f[row+4]*C2, f[row+8]*C3, C4}`
  where `C` = `f[0x209A370..0x209A37C]` — **the same 0x209A370 block
  `3ECFD0` initializes during `26E960`/`26E8D0`** (the scale quad is
  nav-state, BSS/runtime-set — 0 in image; planted in fixture).
- If null: quad = the same `f[0x209A370]` block verbatim (unreachable
  via index 0 — `37AD10(0)` never returns null).
- Template: `d[+0]=0x1042006` (→`b[rec+0x20]` = **kind 6**),
  `b[+4]=1`, `b[+5]|=0x80`, `b[+7]=(b&3)|0x20`, quad at `+0x10`.
- `3AB960(tpl)` → `ebx`; frees old `d[0x2ADD11C]` via `3ABCA0` if
  nonzero; stores `d[0x2ADD11C]=ebx`. Real stack-cookie check.
- Proven: quad `(4,1.5,16,7)` from scale `(2,.5,4,7)` × cfg `(2,3,4)`,
  free called with old `0x3333`, store lands.

## `37AD10(i, &out)` — nav config table

- `i < 5` → `*out = 0x2EBF460 + i*0x50` (5 rows × 0x50).
- `i >= 5` → `*out = 0`.
- **Negative index reads before the table** (`jge` is signed;
  `i=-1` → `0x2EBF410`) — authentic quirk proven.

## `3AC920(payload)` — in-place derived-field recompute

Same kind dispatch as `3AB960`'s inline math (`b[rcx]−2` chain,
shared `K=1.0f`), but operating on the payload view with outputs
shifted −0x20 vs the rec view: kind2→`f[+0x30]=K/x²`, kind3→`+0x40`,
kind4→`+0x48`,`+0x4C=K/(f40−f44)`, kind5→`+0x30/+0x34/+0x38/+0x3C`.
**Kinds 0,1,6,7 → no-op** — explains why `3ABB60`'s builtin kind-7
record takes no derived fields. k4/k5/k7 arms proven.

## `1D50D0`/`17D490` — generation singleton

- `1D50D0` = lazy singleton: `q[0x1F81428]` or
  `210ec0(0x10E8)`→`1CCB20` ctor→store. Early-out branch run real.
- `17D490` = `d[singleton+0xAAC]` — the nav-generation dword
  `265920` prefers. Proven: planted `+0xAAC`=9 → ret 9.

## Corrected cells (read-trace, same slip class)

- cfg table `0x2EBF460` (was computed `0x2EAF460`)
- scale quad `f[0x209A370]` (was `0x20A3370`) — nav-state block
- singleton `q[0x1F81428]` (was `0x3B01428`)
