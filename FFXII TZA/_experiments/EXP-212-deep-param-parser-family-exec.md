# EXP-212 — tag-15 deep param-parser family, executed

**Status:** complete — **519/519 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`dc081df2fc7094b4ab8a8eb09a83452ba497b8083c6ef63fbb487a6902f94b2f`), zero
unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..211; 503 inherited + 16 new `c5f0-*` cases, 21 re-fixed cases with
real param bytes)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

EXP-211 stubbed the nine deep parsers the tag-15 sub-arms call (`3FFEE0`,
`3FFBC0`, `3FFD70`, `3FFC60`, `3FFCE0`, `3FFDA0`, `3FFB00`, `3FFB90`,
`3FFF10`) because they were fixture-dark. Disassembly this round showed all
nine are tiny leaf byte-parsers — seven pure, two (`3FFBC0`, `3FFB90`)
calling only the already-promoted `39BA00` escape lookup. All nine now
execute as shipped bytes, and every previously dark kind arm
(`*` icon, `.` `l` `m` `n` `8` `9` `:` `<` `=` `>` `?`) is exercised with
real parameter bytes.

## Bodies promoted real this round

| body | role | semantics |
|------|------|-----------|
| `003FFEE0` | `"` quoted-skip | scans `b[+1..]` skipping `\x22`-quoted runs to a NUL/`0x0D` bound; optional `w` out at `state+0x9E`; ret = bytes consumed |
| `003FFBC0` | `)` colour decode | `b[+1]&7==0` → escape via `39BA00` (5-byte record reverse-assembled into `d[out]`); else direct pack of `b[+1]`/`b[+2]` shifted nibbles; ret = count |
| `003FFD70` | `*` icon header | `w[r9]=b[+1]&0x7F` (width → `rsp+0x44`), `w[r8]=b[+2]&0x7F` (len → `rsp+0x48`), `q[rdx]=rcx+3` (rest ptr); ret = `w48+3` |
| `003FFC60` | `-` param | byte/nibble field decode into two stack-passed outs; ret = count |
| `003FFCE0` | `.` param | field decode, stack outs; ret = count (arm `0x0C` exits early when `state+0x70==0`) |
| `3FFDA0` | `3` scale pair | `f[r8]=b[+1]/f[0x8F8180]`, `f[r9]=b[+2]/f[0x8F8180]` — shipped const `10.0f`; ret 3 |
| `003FFB00` | `o`/`8` word | direct/escape word decode via `3FFAB0`-style bytes; `o` feeds `float(movsx)`, `8` feeds `2639E0` |
| `003FFB90` | `m`/`n` skip | param-skip variant; ret = count |
| `003FFF10` | `1` skip | param-skip variant; ret = count |

New boundary stubs for the deep tails (disclosed): `263990`, `2B41F0`,
`2AE450`. (`39BA30`, `2AE610`, `2AEB20`, `2B4730`, `2A9F00`, `2B43C0`,
`2639E0`, `17FD30`, `2B1ED0`, `3A1DB0` remain scripted from EXP-211.)

## Newly exercised arms (kind → arm → behavior)

| sub | kind | behavior |
|-----|------|----------|
| `.` `0x2E` | 0x0C | `3FFCE0` field decode; `q[state+0x70]==0` → early ret-1 tail (`f2e`) |
| `l` `0x6C` | 0x1E | `3FFCE0` parse → `2B4730` boundary, field writes (`f6c`) |
| `m` `0x6D` | 0x1F | `3FFB90` pure param skip (`f6d`) |
| `n` `0x6E` | 0x20 | `3FFB90` pure param skip (`f6e`) |
| `8` `0x38` | 0x15 | `3FFB00` word `0x28` → `2639E0(0x28)` stub → 0 → early ret-1 (`f38e`) |
| `9` `0x39` | 0x16 | `3FFAB0` → `b[state+0xAB]` write (`f39`) |
| `:` `0x3A` | 0x17 | `3FFAB0` → `b[state+0xAC]` write → `e598` clear + `17FAE0(0)` tail (`f3a`) |
| `<` `0x3C` | 0x18 | `3FFAB0` → `b[state+0xAD]` write (`f3c`) |
| `=` `0x3D` | 0x19 | `3FFAB0` → `b[state+0xAE]` write (`f3d`) |
| `>` `0x3E` | 0x1A | `3FFAB0` skip → `263990(q[e312+0x78])` stub → 0 → early ret-1 (`f3e`) |
| `?` `0x3F` | 0x1B | `3FFAB0` (param 5) → `0xD0` state copy → `2AE450(copy,5,params)` stub; `b[ctxo+0x10FC]=1`, `bA9=0`, `d[aux]=1` (`f3f`) |
| `*` `0x2A` | 0x08 | `3FFD70` icon header → suppress `rest[w48]` + `rest[w48+w44]` → `2B43C0` ×2; **two unconditional nested `2B2150` walks** on `rest`/`rest+w48`; `ctx48!=0` → icon-fit clamp + `2A9F00` publish + ctxo `d10D8`/`d10DC`/`f10E4` restore (`f2a`/`f2ac`/`f2an`) |

Previously stub-fed cases (`f22`, `f29`/`f29e`/`f29z`, `f2b`, `f2d`, `f31`,
`f33`, `f34`, `f35`/`f35n`, `f36`, `f6f`/`f6fe`, `f32`/`f32a`/`f32b`, `f42`)
now feed real parameter bytes through the promoted parsers — stub return
keys (`fee0n`, `fbc0n`/`fbc0v`, `fc60n`, `ff10n`, `fda0n`/`fda0a`/`fda0b`,
`fb00w`/`fb00n`) deleted.

## Corrections of record

- **The `*` arm's nested `2B2150` calls are unconditional.** `cmp w48, len`
  / `cmp w44, len2` gate only the *byte suppresses* before each call — the
  walks themselves always run, on `rest` and `rest+w48` respectively. A
  heavy byte in the icon blob therefore requires the real decode chain
  (`s2ac2f0` + `q[state+0x60]` flag desc via `e312q` + `eflags`), even when
  the count fields nominally fall outside the blob.
- **The second suppress targets `rest[w48+w44]`**, not `rest[w44]` —
  `rsi = rest + w48`, `rax = movsx(w44)`, `b[rax+rsi]` suppressed.
- **`3FFD70`'s icon sub-record layout** confirmed by execution: `w44` =
  width byte, `w48` = blob-length byte, `q[+0x60]` out = `rest` =
  `cursor+4`; consume = `len+3`.
- First-pass fault (`0x2B22F1`, `mov ecx,[rcx+0xC]` on a null record ptr)
  was the unconditional nested walk hitting `'A'` heavy-decode with an
  unplanted `q[copy+0x60]` flag-desc — fixed by the `e312q={0x60:"c60"}`
  fixture (copied into the `rbp-0x70` state copy), `c2f0=[(3,1)]`, and
  `eflags={3:0x80000000}` — the same chain `b2150-heavy` exercises.

## Not claimed

`live_game: false`. `263990`, `2B41F0`, `2AE450`, `39BA30`, `2AE610`,
`2AEB20`, `2B4730`, `2A9F00`, `2B43C0`, `2639E0`, `17FD30`, `2B1ED0`,
`3A1DB0` remain disclosed scripted boundaries. The `*` icon-fit clamp reads
`2B43C0` stub returns; the `>`/`?` publish paths (`263990`/`2AE450`) are
stub-bounded. The `l` arm's `2B4730` tail and the `8` arm's `2639E0`
nonzero path execute native but stay fixture-dark.
