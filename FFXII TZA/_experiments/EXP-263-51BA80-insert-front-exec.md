# EXP-263 — `0051BA80` record-insert front: capacity gate + populate-fail arms

**Status:** complete — **580/580 cases, stable across 3 independent
runs, byte-identical `result.json` (SHA256 prefix `d7f7cf78`;
580 cases), fault census 26** (unchanged from EXP-262).
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes
executed under Unicorn on the `dcntr` fixture plus a new `src`
(arg5 source-spec) fixture; nothing claims initialized-gameplay
reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py`
(extends EXP-192..262).
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

**Correction of record:** the "deeper `0051BA40` body" in EXP-262's
plan was misattributed — `0051BA40` ends at `0x51BA76`; the deeper
body is `0051BA80`, a distinct 5-arg function (the **insert**
complement of `0051BA40`'s delete).

## `0051BA80(C, edx, rsi, ebp, r14)` — insert/replace

```
if edx == -1:                          # auto slot
    eax = 51F150(C)                    # cap gate: d[C+0x14]>=d[C+0x10]
    if eax < 0: ret -1                 #  -> -10 -> ret -1
41CB90(&tmp)                           # stack 0x390-record reset
eax = 41D220(&tmp, r14)                # populate from src spec
if eax == 0:                           # populate failed
    if ebx != -1:                      # replace an existing slot?
        rax = 51F240(C, ebx)           #   resolve desc
        41CF00(record)                 #   reset its record
        51F190(C, d[record])           #   release by record key
    ret -1
if ebx == -1:
    ebx = 51F080(C, rsi, ebp, 0)       # alloc: marks desc, links it
    if ebx < 0: ret -1
rax = 51F240(C, ebx)                   # desc -> record ptr
copy 0x390 bytes &tmp -> rax           # 7x0x80+0x30 movups loop
41CA70(record)                         # tail fixup
d[record] = ebx                        # stamp the key
ret ebx                                # key = slot|0x10000
```

Callee semantics pinned while tracing (all read in shipped bodies):

- **`51F150(C)`** — capacity gate: `d[C+0x14] >= d[C+0x10]` →
  `-10`; else returns `d[C+0x18]` (the free-slot cursor).
- **`51F410(C)`** — allocator pick used by `51F080`: same cap gate,
  `d[C+0x14]++`, returns the *entry* cursor `esi`, then scans the
  `0x30`-stride desc array for `d[desc]==0` and leaves `d[C+0x18]`
  pointing at the next free desc (or 0 on wrap / when full).
- **`51F080(C, rdx, r8d, r9d)`** — alloc + link: resolves the desc
  array (mode 0 via `3AB7F0`, mode 1 direct), `d[desc]|=1`
  (`|=2` when `r9b&2` — the `&2` lazy-record flag's producer),
  `d[desc+4]=slot|0x10000`, `q[desc+0x10]=rdx`,
  `d[desc+0x20]=r8d`, **pre-resolves** `q[desc+0x18]=
  sx(3AB7F0(rdx)+r8d)` (the same formula `51F240` re-runs on `&2`),
  then `51F380(C, key)` tail-links and returns the key.
  `zx`/16-bit indexing strips the `0x10000` tag bit — the key's
  high bits are a generation/tag namespace.
- **`51F380(C, key)`** — empty list (`d[C+0x20]==-1`) →
  head=tail=key; else patches `d[tail+0xC]=key`,
  `d[new+8]=d[tail+4]`, `d[C+0x20]=key`.
- **`41D220(rec, src)`** — deep populate: `d[rec+0xC]|=0x100001`,
  `w[rec+0x318]=w[src+0x10]`, `w[rec+0x31C]=w[src+0x20]`,
  `q[rec+0x310]=q[src]`, `q[rec+0x330]=q[src+8]`,
  `d[rec+0x338]=d[src+0x14]` (seeds the `0x1000`-arm container of
  EXP-262), `b[rec+0x2DC]=0xFF`, `409210(rec+0x2EC, q[src+0x18])`
  (0x20-byte obj init), `409F50(q[src], w[src+0x10])` = the
  `2ED570` doc-resolve wrapper (`dx==-1` → 0) → `409A30`/
  `409660` tagged-section scans (`"CMF@"`/`"PRF@"`/`"MRF@"`,
  via `409780` → `409C30` per-section matcher) → `41CA70` →
  `41CD30`/`46E420` → ret 1 only when `q[rec+0x368]` got set.
- **`41CA70(rec)`** — `q[rec+0x18] = rec+0x30 +
  sx(d[rec+0x20])*0xA0` (current-block pointer); when
  `b[rec+0xC]&0x20`==0 and `w[rec+0x318]`!=-1, resolves
  `q[rec+0x368]`/`q[rec+0x370]` through the
  `409F50`/`4096C0`/`4090D0` chain; per-block `w[base+0x3A]==1 &&
  w[base+0x50]!=-1` rows get `q[+0x70]`/`q[+0x78]` resolved.
- **`409780`/`409660`/`4096C0`/`4090D0`** — all null-safe on the
  doc pointer (`test rbx/rcx; je` early-outs). `409780` always
  runs `409210(0x2B62E20, r8)` when `r8`≠0.
- **`46E420(C, slot)`** — `edx==-1` → early-out; else
  `2ED570` → `3713C0` — bounded.
- **`409210(obj, arg)`** — zeroes `obj`'s 0x20 bytes, calls
  `ff15[008C2F70]` (an unbound import thunk — value `01CCEF16`
  is data, not code), then `b[obj+0x1F]=0`. **The IAT slot was
  planted to a heap `ret` byte** — a disclosed synthetic import
  boundary; the lock-init semantics are nil for the fixture and
  every shipped instruction of `409210` still executes.

## Cases and pins

- **`d51ba80-cap`** — `edx==-1` with `d[C+0x14]`≥`d[C+0x10]` →
  `51F150` ret `-10` → ret `-1`; no desc marked, count untouched.
- **`d51ba80-pop0`** — `edx==-1`, `w[src+0x10]=-1` → `409F50` ret 0
  → null doc → two `409780` section scans (each running `409210`
  on the `02B62E20` static — sentinel overwrite pinned) →
  `409660` ret 0 → `41CA70` (gates skip) → `41CD30`/`46E420`
  early-outs → `41D220` ret 0 → `ebx==-1` → ret `-1`; **no desc
  allocated** — `51F080` never runs on a `-1` index with failed
  populate.
- **`d51ba80-dereg`** — `edx=1`, same failing src → populate ret 0
  → `51F240(C,1)` → `41CF00` resets the live record → `51F190`
  releases desc `A[d[rec]]` → ret `-1`. **Populate failure on an
  existing slot deregisters it** — same reset+release shape as
  `0051BA40`'s delete.

## Not claimed

- The happy insert path (`51F080` alloc + `0x390` copy +
  `41CA70`'s `q[+0x368]`/`+0x370` resolution) — needs a planted
  `2ED570` document container + `PRF@` section directory +
  matching `409C30` section row + `q[tmp+0x330]` container chain;
  deferred to a dedicated package (same class as the `5369C0`/
  `3B02A0` fixtures),
- `41D220`'s section-hit internals (`d[rec+0x320]`/`+0x378`/
  `+0x37C`, `409C30` param-match rows), the `46E420`→`3713C0`→
  `3E18D0` live path, `0041CFC0`'s block — `NATIVE-REPLAY`,
  `live_game: false`,
- the import thunk's real semantics (`q[0x8C2F70]` planted `ret` —
  the boundary is recorded, not hidden).
