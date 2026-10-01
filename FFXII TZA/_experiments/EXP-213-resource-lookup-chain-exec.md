# EXP-213 — tag-15 resource-lookup chain (`39BA30`/`263990`/`2639E0` + `32A930`/`3EAC10`), executed

**Status:** complete — **521/521 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256
`2b0f36d44e8ab00e7122b76300a6e9c8c9cc16838cb8947aab69693ad7a1c5f6`), zero
unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..212; 519 inherited + 2 new `c5f0-*` deep-path cases, 4 re-fixed)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

EXP-212 left the resource lookups the `!`/`8`/`>` arms call scripted.
All five turned out to be thin resolvers over runtime tables — promoted
real along with the two callees they chain into (`2EF2B0`/`2EF640` were
already real). The `8`/`>` arms' deep tails (resolved-resource embed)
now execute native for the first time.

## Bodies promoted real this round

| body | semantics |
|------|-----------|
| `0039BA30` | font-record lookup: `rec = q[0x2AEE810 + 8·cl]` (table INLINE at fixed BSS, not a pointer); `edx==0` → `d[rec+0x40]&0x18000 ? 0 : rec+0x40`; `edx!=0` → `254A10()==0` → `rec+0x40`, else scan `w[rec+6]` records chained by `d[rbx]` from `rec+0x10`: `w[rbx+0xC]>0x30 && (d[rbx+0x30]&0x18000)==0x8000` → `rbx+0x30`, exhaust → 0 |
| `00263990` | `>` named-record resolver: `w[rcx+0x102]<0` → `q[rcx+0xF8]` direct ptr; else `3EAC10(btr(w102,0xE), 32A930(...))` |
| `002639E0` | `8` index resolver: `32A930(ecx&~0x4000)` bit-test → `3EAC10(ecx, bit!=0)` |
| `0032A930` | alloc-bitmap bit-test: `0≤ecx<0x800` → `b[0x2164480 + (idx>>3) + 0x13B4] & (1<<(idx&7))` — `2EF2B0()` = `0x2164480` (= `2EF640()` global `0x2164280` + 0x200) |
| `003EAC10` | pair-table lookup: `edx = 2·ecx + setne(flag)`; `tab = q[0x2B5E0D8]`; `d[tab+8] > edx` → `movsx(d[tab+0xC + edx*4])`, else 0 — **returns a dword the arms treat as a resource string pointer** |

## Semantics now executed

- **`!` font select (`f21`/`f21a`)**: real `39BA30(bA6, 1)` over the
  `ba30t` fixture — `254a10==0` → `rec+0x40` (`q68`/`q60` set); the
  `f21a` variant runs the `w6` record-scan to a matching entry
  (`wC=0x40>0x30`, `d30&0x18000==0x8000` → `rec+0x40`), then the arm's
  own `254a10==1` → `17FD30(bA6,1)`, `cc30=bA6`, `cc34=1`.
- **`8` arm (`f38e`/`f38n`)**: `3FFB00` word → real `2639E0(0x28)` →
  `32A930` bitmap + `3EAC10` table. `f38e`: unplanted table → 0 →
  early ret-1. `f38n`: `eac10t[0x50] = rstr` → the **resolved-resource
  deep tail** — `0xD0+0x80` state copies, NUL-scan `r13`, suppress
  `r13[len]` (the NUL — count fields off-by-one by design),
  `2B41F0(r13)` measure → `w[rbp+0x1c]`, unconditional nested
  `2B2150` on the resource string (real decode via `e312q0x60`/`c2f0`/
  `eflags`), then the shared publish: ctxo `d10D8`/`d10DC`/`f10E4`
  saved, `2A9F00` boundary, `f[cc68]`/`f[cc64]` outs, restore,
  `d[q[rsp+0x60]] = movsx(w1c)`.
- **`>` arm (`f3e`/`f3en`)**: real `263990(q[e312+0x78])` — `f3e`:
  `w102=0` → `32A930(0)`/`3EAC10(0,0)` → 0 → ret-1. `f3en`:
  `w102=0x8000` → `q[nobj+0xF8]` direct → same deep tail as `8`.

## Corrections of record

- **`3EAC10`/`2639E0`/`263990` return dword table entries used directly
  as string pointers** — `movsxd` sign-extends; planted VAs must stay
  `< 0x80000000`.
- **`39BA30`'s table is INLINE at `0x2AEE810`** — `lea` loads the base
  address itself (unlike `39BA00`'s `q[0x2AEE870]` pointer). Fixture
  writes entries at `0x2AEE810+8·idx` directly.
- **Fixture ordering:** `e312q`/`nobjq`/`eac10t` resolve alloc names —
  `nobj`/`rstr` must be allocated before the `e312q` preset loop (the
  first pass left `q[e312+0x78]=0` → `263990` faulted on `w[0x102]`).

## New fixtures

- `ba30t {idx: {"w6": n, "e": [(stride, wC, d30), ...]}}` — font rec
  alloc'd per idx at `q[0x2AEE810+8·idx]`; record chain at `rec+0x10`.
- `a930m {byteoff: byte}` — `32A930` bitmap bytes at `0x2175834`.
- `eac10t {i: val}` / `eac10n` — `3EAC10` pair table at `q[0x2B5E0D8]`.
- `nobj`/`nobjw`/`nobjq` — the `>` arm's `q[e312+0x78]` record object.
- `rstr`/`rstrb` — the resource string the `8`/`>` deep tails consume.

## Not claimed

`live_game: false`. `2B41F0`/`2B43C0` (the measure wrappers),
`2A9F00` (publish), `2AE450` (`?` sprite draw — `39BB00`/`2AFDC0`
chain), `2AE610`, `2AEB20`, `2B4730`, `3A1DB0`, `17FD30`, `2B1ED0`,
`2639xx` siblings remain disclosed scripted boundaries. The runtime
tables (`0x2AEE810` font recs, `0x2B5E0D8` pair table, `0x2175834`
bitmap) are fixture-planted — real game content differs. The `>`
deep tail's `d[q[rsp+0x60]]` out-write lands on a stale stack cell
(not assertable); the `8` arm's own head variant (`d44|=4` path)
isn't separately cased.
