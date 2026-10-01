# EXP-210 — `002AC5F0` remaining dispatch arms, executed

**Status:** complete — **466/466 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`8b72187060056bede0e867c02b91b874a718dabf491813b2a61da7ded83cf856`), zero
unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..209; 455 inherited + 11 new `c5f0-*` arm cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

EXP-209 promoted `002AC5F0` but exercised only tags 2/3(indirect)/5/8/9/
11–13/14/15 boundary paths. This package exercises **every remaining
arm** through direct `2AC5F0` entry (`rdx = &cursor` cell — new `ccp`
fixture). No new bodies were promoted — the five leaf helpers went real
in EXP-209; this round only adds fixtures and cases.

## Register bindings (from the prologue)

`r14` = `rcx` = state (`0xD0` struct) · `rdi` = `rdx` = &cursor cell ·
`r13` = `r9` = aux dword out (`d[r9]=0` at entry, `1` on productive
arms) · `r12` = `r8` = params float block · `r8` reloads
`q[0209CC40]` = the **global** text ctx (`ctxo`) · `r15` = 0 ·
`rsi` = image base for the jump tables.

## Arm semantics now executed

| tag | arm | executed behavior |
|-----|-----|-------------------|
| 1 | `0x2ACB96` shared | `17F920(ecx=0)` → `eax` → `xmm7`; `+f[state+0x4C]`; `×f34 ×f38` → `f[cc68]`; height `int(17F880)` `×f34 ×f3C` → `f[cc64]`; `d[aux]=1`, cursor+1, ret 1 (`c5f0-tag1`: `5·2·3=30.0`, `6·2·4=48.0`) |
| 4 | same | identical but `17F920(ecx=1)`; `d[state+0x44]&0x800 && b==4` adds shipped `+1.0f` (unexercised branch — needs `d44` bit) |
| 6 | same | advance = shipped const `f[0x8F8180] = 10.0` (`c5f0-tag6` → `60.0` under `2·3` scale) |
| 7 | same | `229E40()==7 ? 0x1A : int(24ABA0()·10.0)` — the `d[01E02E14]==7` gate selects fixed `26` vs computed `10` (`c5f0-tag7`/`tag7a`, new `e2e14v` fixture) |
| 2 | `0x2AC6D1` | `b[ctxo+0x10FC]=0`, `b[ctxo+0x1102]=1`; **nested `2B2150(state, cursor+1, &w, &h)`**; `f[params] = 2B1F20(state) + 2B2C50(state)`; `f[params+4] += d[0209CC3C]·f34·f3C + nested_h` and `f[ctxo+0x10E8] = nested_h` when `nested_h != 0` (else `f[ctxo+0x10E8]` takes its place in the sum); clears `q[0209CC60]`/`q[0209CC68]` and `q[0209E598]`; `b[state+0xAA] > 0` (signed) overrides `f[params]` with `float(byte)`; `q[state+0x20] != 0` → tail block `17F850` + `17FA10(q[state+0xB8], 0x44, 1)` + `2AB820(d[0209CC30], d[0209CC34])` + `17FB00(q[state+0x20])`; **returns 1** (`c5f0-tag2`/`tag2f`) |
| 3 | `0x2AC6AE` | cursor+1, clears `q[0209E598]`, `b[ctxo+0x10FC]=0`, `17FAE0(0)`, **returns 0** — the line-break terminator (`c5f0-tag3`) |
| 10 | `0x2ACE25` | tag-5-family advance (`15.0` shipped) then a byte scan from `cursor+1` stopping at `\x00`/`\x02`/`\x05` — a `\x05` hit is **nulled in the buffer** (`b[rbx]=0`) before the nested `2B2150(cursor+1, &f)` and restored after — i.e. the run is measured with the next tag suppressed; `f10F0 = max(f10F0, nested_w)`, `f10F8 = f10F0 − nested_w` (`c5f0-taga`) |
| 15 | `0x2AD01A` | cursor+1 stored, then re-dispatches on `b[cursor]` through a **second-level** pair: kind byte `b[base+0x18E3FC+idx]` + jump table `d[0x2AE370+4·idx]` for `idx = b−0x20 ≤ 0x50`; out-of-range → ret-1 tail (`c5f0-tagf`, `0x80`) |

Already-executed in EXP-209: tag 5 (`15.0`/`6.5`, `b10FC=0`,
`b1100=1`, nested `2B2150` under `ctx48==0`), tags 8/9 (cursor +3/+1),
tags 11–13 (no-op ret 0), tag 14 (`3FFDF0`/`2B2DF0` boundaries, `b1101`
+`b10FE`, ret 0), NUL and match-word exits.

## New fixtures

- `ccp` — a cursor cell (`q[ccp] = nstr`) so direct `2AC5F0` entry
  takes `edx="ccp"`.
- `f920v` — return value of the scripted `17F920` metric source
  (tag-1/4 advance; default `0`).
- `e2e14v` — the `d[01E02E14]` BSS dword `229E40` reads (tag-7's `==7`
  gate; ships `0`).
- `e312f {0x34,0x38,0x3C}` — the three state scale fields the
  advance/height math multiplies through.

## Corrections of record

- Tag 2 **returns 1** (continue), not 0 — the nested-measure arm exits
  through the `17FAE0`+`mov eax,1` tail at `0x2ACFBB`, not the
  `xor eax` ret-0 path.
- The shared arm's height is **`cvttss2si(int)` then scaled by
  `f34·f3C`** — a different second scale (`+0x3C`) than the advance's
  `f34·f38`, and integer-truncated unlike tag 5's float height.
- Tag 10 **mutates the string buffer**: it stores `0` over the found
  `\x05`/`02` for the nested measure and restores it — a real
  write side-effect on the caller's text.
- `rsi` inside the shared arm = `q[0209E598]` (the same cell the
  walkers save/clear) — the kern/bitfield branch (`rbx` font vs `rsi`
  glyph-pair bitfield, `>>20`/`>>14`+`&0x1F` −3, bias `394282.25f`)
  stays fixture-dark under `e598v=0`.

## Boundary status

Unchanged from EXP-209 — no new bodies promoted. All scripted
boundaries (`002A9F00`, `002B2DF0`, `002B43C0`, `002AB820`,
`003FFDF0`, `002B3E30`, `002AC2F0`, `17Fxxx` family) remain disclosed
stubs; the tag-15 sub-arms themselves run native but need their own
fixtures to exercise meaningfully.
