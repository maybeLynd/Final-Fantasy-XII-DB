# EXP-260 — `002ED570` arm variants + `003AB7F0` handle resolve (direct entry)

**Status:** complete — **566/566 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 prefix `2b472799`; 566
cases), fault census unchanged at 20** (the same pre-existing
intentional-null fixtures).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn on the extended `dcntr`/`c2` fixture; nothing
claims initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..259).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Correction of record (supersedes EXP-259's `003AB7F0` sketch)

EXP-259 described `003AB7F0` as "low-2-bit tag: `0`=direct,
`1`=`0036B130` id resolve, `2/3`=null". The body is:

```
rcx == 0            -> ret 0          (caller-side: 2ED570 checks
                                       q[C2+0x30]/q[C2+8] != 0
                                       before calling at all)
(dl & 3) == 0       -> ret rdx        (aligned = direct pointer)
(dl & 3) != 0       -> 36B130(edx);   movsxd rcx, eax;
                       rcx <= 0x40    -> ret 0  else ret rax
```

**Every nonzero low-2-bit value resolves through `0036B130`** — the
tag bits are only "not a pointer"; there is no tag-2/tag-3 null arm.
`0036B130(ecx)` itself: `ecx==0`, `cl&3==0`, `ecx<0x100000`, or
`(ecx&~3)==0` → ret 0; else `ret q[ecx&~3 + 8] + 0x40` — a handle is
`header | lowbits`, resolving to `q[header+8]+0x40` (a 0x40-byte
block-header skip). All arithmetic is 32-bit: handles must live below
4 GiB. `d422c20-18tag` exercises tags 1 and 3 resolving identically;
the EXP-259 record and §13bp are corrected.

## Arms newly exercised (all shipped bytes)

- **`d422c20-18sh`** — the sub-array index is `slot >> d[C2+0x4C]`
  (`sar ebp,cl`), while the **row index is the raw slot** (`rsi<<4`).
  `shift=1, slot=1` resolves `subs[0]` while gating on `rows[1]` —
  pinned asymmetric indexing.
- **`d422c20-18mm`** — `ret = element + (d[C2+0x50] & slot) *
  d[C2+0x48]`: `mask=1, mult=0x10` lands the `&=~8` at
  `element+0x10`; `d[element+0]` stays `0xF`. The mask×mult tail is
  an element-relative write offset, not a row/slot count.
- **`d422c20-18tag`** — `q[C2+0x30] = hdr|1`, `q[C2+8] = hdr|3`
  (planted `q[hdr+8] = base-0x40` headers): both bases resolve
  identically to the direct-pointer result. Tag value is
  insignificant — the pins are `q[C2+0x38]==rows`,
  `q[C2+0x10]==subs`, `d[E2] 0xF→7`.
- **`d422c20-18noc`** — null `q[C2+0x30]`/`q[C2+8]`: the `003AB7F0`
  calls are skipped (`test rcx,rcx; je`) and the resolved cells
  `q[C2+0x38]`/`q[C2+0x10]` keep their **cached** bases — a
  re-resolve only overwrites the cache when a tagged base exists.

## Cases

`d422c20-18sh`, `d422c20-18mm`, `d422c20-18tag`, `d422c20-18noc` —
each keeps `d[elem+0xC4]`/`d[+0xC8]` = -1 (the EXP-258 arms stay
skipped), `d[+0x18]=1`, and shares the EXP-259 pins: bases stored,
`d[elem+0x18]` never retired, clear block identical.

## Not claimed

- `0036B130`'s rejection paths (`ecx<0x100000`, `(ecx&~3)==0`,
  resolved `eax<=0x40` → `003AB7F0` ret 0 → resolved-cell overwrite
  with 0 and the consequent low-memory row read),
- `002ED610`'s caller (`d[elem+0x84]`-offset second container walk,
  `0x290`-stride row tail),
- `0051BA40` mode-0/`b[desc]&2` arms, `0041CF00`'s `w[R+0x28]`/
  `d[R+0xC]&0x1000` arms, `005369C0`/`003B02A0` real,
  `q[02EBF188]` consumers, live-game reachability —
  `NATIVE-REPLAY`, `live_game: false`.
