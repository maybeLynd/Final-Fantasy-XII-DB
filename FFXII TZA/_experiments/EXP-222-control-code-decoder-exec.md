# EXP-222 — `2AC2F0` control-code/char decoder + `254A10` lang check real

**Status:** complete — **540/540 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256 `ff908d9c` prefix; 540 cases),
zero unexpected faults** (the 10 faulted cases are the same pre-existing
intentional-null fixtures that assert the fault).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..221; 0 new cases this round — retargeted 9 existing
decode cases onto real byte streams)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Bodies promoted real this round

| body | semantics |
|------|-----------|
| `002AC2F0` | 187-insn control-code/char decoder. Head clears `q[0x209CC70]`/`q[0x209CC78]`. `al = b[q[rdx]]` (the byte at the caller's cursor): **≥0x20** → `esi = al−0x20`, `39C4A0(0)` font record → `q[ctx+0x60]`, `17FD30` scripted setter (`ecx = 7 or 0` on `d[ctx+0x44]&0x800`, `r8d = d[0x209D480]`), `d[0x209CC30]`/`+34` mode globals, cursor **+1**. **<0x20** → `r8d = d[(d[0x209CC38] ? 0x9165B0 : 0x916570) + (al&0xF)*4]` (two shipped 16-dword base tables), `esi = b[cursor+1]−0x20 + base`, cursor **+2**; tag-vs-`d[0x40E6F9]` bound is never `jae` in replay (shipped dword `0x0FF32C24` > any byte). Tail `0x2AC461`: metric pair `17F980/17F960` (d44&0x800) or `17F8A0/17F880` → `f[0x209CC70]/+74`; `r14 = 20E600(d[rec+0xC]) + esi*8` element record → `q[0x209D698]`; `rbx = 17F8C0(esi)` glyph remap; `d[r14]&0x80000000 && f[ctx+0x40]≠0` → `xmm6 = f[0x90393C]` (shipped 0.0), overridden by `f[0x1CEBB70]` only when `254A10()==0`; kern: `rbx` → `17F9C0(d[rbx+0x1C])` else `(q[r14]>>0x20)&0x1F` fallback; `+f[ctx+0x4C]+xmm6` → `f[0x209CC78]`; `17F940()≠0 && rbx≠0 && d[rbx+0x20]≠−1` → `17F8E0(d[rbx+0x20])` kern2 → `f[0x209CC7C]`; `17FAE0(rbx)` publishes the glyph record into `q[dev1+0x28]`; `xmm[0x209CC60] = splat(f[ctx+0x34]) * [0x209CC70..7F]` quad; `f[ctx+0x38]`/`f[ctx+0x3C]` ≠ 1.0 → rescaled quad + `f[0x209CC64]`; `b[ctx+0xA9]`≠0 → `f[0x209CC68] = float(bA9)`, clears bA9. Returns `eax = esi` (decoded element index). |
| `0017F8E0` | kern-pair thunk: `1B5FA0()` → `1E9780(dev1, ecx)` → `1B5FA0()` → `1E9BD0(dev1, eax)` → `cvttss2si`. |
| `001E9780` | two-gate forwarder: `q[dev1]` (devsub) and `q[dev1+0x28]` (saved ctx) both nonnull → `1FDDD0(devsub, r8d=edx_arg, edx=d[ctx+0x20])`; else 0. |
| `001FDDD0` | two-level std::map find: outer map `q[rcx+0x88]` root / `rcx+0x78` sentinel keyed by `r8d`; inner map `q[node+0x40]`/`node+0x30` keyed by `r10d`; returns `d[node+0x24]`, 0 on miss. |
| `00254A10` | language-set check: `229E40()` → `d[0x1E02814]` ≤ 0xB and `bt 0xD81` → 1 iff lang ∈ {0,7,8,10,11}; else 0. **55 live call sites in-suite.** |

## Corrections of record

- **`254A10`'s stub polarity was inverted for lang 0.** The scripted
  default returned 0 for every case that did not plant `s254a10_ret`;
  the real body returns **1** for `d[0x1E02814]==0` (0 is in the
  `{0,7,8,10,11}` set). Every `254a10==0` arm in the suite was being
  exercised under a value the shipped body never produces for default
  state. Cases asserting `254a10==0` arms now plant `e2814v=1` (bit 1
  clear in `0xD81`).
- **`c5f0-tag7a` exposes a dead shipped arm:** `e2814v=7` makes
  `254A10()` return 1 (7 ∈ the set), so the arm sequence
  `254a10()==0 && 229e40()==7 → param 0x1A` can never fire for lang 7 —
  the `0x1A`-special is unreachable by construction. Real result is the
  `24ABA0` `int(1.0*10.0)` arm → `cc68 = 10*2*3 = 60`, not the
  stub-fiction 156.
- **The decoder publishes `rbx` into `q[dev1+0x28]`** via `17FAE0` —
  the walkers' save/restore slot is *written* by each decode, not just
  read. Subsequent `17F940()` reads see the last glyph record pointer.
- **`2AC2F0` consumes the cursor itself** (`+1`/`+2`), not the caller —
  the stub's per-case advance fiction (`c2f0` pairs) is retired; all
  decode sites now run on the real bytes (`\x23`→esi 3, `\x24`→4,
  `'A'`→0x21).
- **`17F8C0` fires twice per heavy char** in `b2150-*` — once inside the
  decoder's publish tail, once in the walker's own flag test.

## Retargeted cases (no count change)

`b2150-heavy`/`b2150-adv`/`af340-heavy` (`\x20`→`\x23` lead byte),
`c5f0-f38n`/`f3en` (`rstrb` `X`/`Y`→`\x23`), `c5f0-f2a`/`f2ac`/`f2an`
(blob byte `\x41`→`\x23`), `b1fb0-dec` (`'A'` real decode → esi `0x21`,
consumed 1, glyph-map miss → `(q[r14]>>0x20)&0x1F` fallback arm), plus
`e2814v=1` on `b3050-arm`/`c5f0-f21`/`f28`/`f37`/`f20k` and
`devctxv="devctx"` on every glyph-hit decode case so `17F8E0`'s
`d[q[dev1+0x28]+0x20]` reads a real object instead of the opaque
`0x1234` placeholder.

## Still scripted (disclosed)

- `s17fd30` (×19) — the `'!'`-arm font-mode setter shim inside the
  decoder and callers; target `1E9D20` (122 insns, 6 deeper callees) is
  the next sibling-thunk candidate.
- `s17f850`/`s17fa10`/`s17fb00`/`s2ab820` — other sibling shims.
- `scrtfmt`, `salloc`/`sdealloc`, `s2alloc`/`s2dealloc` — sinks.
- `s181330` (×2) — `1B03D0` emit-tail op.
- `s39bad0`, `s3ffdf0`, `s2b2df0`, `s2b3e30`, `s313f60`, `s323c60`,
  `s7930`, `s71c0`, `s2699d0`, the `s53690`/`s54ee0`/`s69e80`/`s9490`/
  `s7090`/`sfb80`/`s7ed0`/`s6a50`/`s80f0`/`s9ca0` family — unrelated
  stat/measure boundaries untouched this round.

## Stability

- `540/540` PASS, three consecutive runs, identical `result.json`
  (`ff908d9ca84c617f…` sha256).
- Faulted cases: none in `result.json`.
