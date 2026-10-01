# REVIEW: SD-184 pair — heading-range (OPUS) + facing-sources (ORACLE)

- **Packages:** `sd184-heading-range-0930` (OPUS `50890aa7f`) and
  `sd184-facing-sources-0930` (SWE2-ORACLE `8acf79ac7`)
- **Tasks:** `OPUS-REQ-AUDITSPEC-SD184-0930`, `ORACLE-REQ-AUDITSPEC-SD184-0930`
- **Reviewer:** SWE2-AUDIT-SPEC (independent of OPUS and ORACLE)
- **Verdict: ACCEPT (both)**

## Controls re-run

- OPUS `sd184_range.py` → `rerun_sd184_range.out`: identical, `FAILS 0`.
- ORACLE `sd184_facing_sources.py` → `rerun_sd184_facing_sources.out`: identical, `FAILS 0` (~57 s).
- ORACLE `sd184_setposparty_census.py` (run as `copy_sd184_setposparty_census.py` so the TSV writes
  into this review dir) → `rerun_sd184_setposparty_census.out` + `sd184-setposparty-sites.tsv`:
  identical to the committed copies, `FAILS 0`.
- All independent derivation used `../auditspec-review-sd193-0930/rvimg.py`, which asserts the
  certified-image sha256 `73461D08…21F8` on load (note: ORACLE's own `img.py` does not assert it).

## Independent verification (not a re-run of the authors' logic)

### The normaliser's defect bands — own Unicorn sweep

`0033CB70` executed over an 80,001-point sweep of [−40, 40] against the shipped bytes:

- 25,132 out-of-range results, clustered into exactly the claimed bands:
  (−12π,−11π), (−10π,−9π), (−8π,−7π), (−6π,−5π), (5π,6π), (7π,8π), (9π,10π), (11π,12π).
  Smallest mis-normalising input: **15.708 = 5π**, matching ORACLE's claim.
- `4π → 0.0` (loop path); `16 → 3.4336` and `−16 → −3.4336` out of range; `13 → 0.4336` in;
  `5.846853 → −0.4363` in — reproduces OPUS's M1 model row-for-row.
- Instruction check: fast path = `x − cvttss2si(x/2π)·2π` at `0033CBCD..E8`; loop path
  bounded to [−π, π] via the two addss loops. Both records' descriptions are exact.

OPUS's necessary condition (|x| > 4π) and ORACLE's tightened band statement are consistent
arithmetic, not a disagreement.

### Store/caller censuses — own .pdata-root scan

- `00310920`: exactly **one** caller (`0037D0D8` in `0037D000`). `xmm6 ← xmm1` at `0031094F`,
  restored only in the epilogue (`00310D0A`); all three `+0x160` stores
  (`00310B00`, `00310BB1`, `00310CA6`) write that raw `xmm6`. Verified.
- `0037D000`: exactly **two** callers — `0035720E` (in `003571A0`, `r8d = 1`) and
  `0033F0DB` (`r8d = 0`). The `test r8d,r8d; jne 0037D0A6` split is exact: flag=1 forwards
  `xmm6` to `00310920`; flag=0 routes through `0026B620`/`0026A0D0`, the wrapping
  movementState setters. `setposparty` stores raw, `setposparty_mapjump` wraps — as claimed.
- `003003F0`: 3 call sites (`00325D5C` ∈ `00325BB0`, `00326F86`/`0032707D` ∈ `00326D60`) —
  matches OPUS's S1.
- `00311F70`: 7 call sites — matches the claimed count.
- `00334120`: 9 call sites, exactly ORACLE's list. Early path at `00334187` returns `xmm6`
  (= arg `xmm1`, the target) raw; both step arms tail-call `0033CB70` (normalised).
- `00265200`: kind byte `[rcx+3] >> 5`; kind 1 → `+[0xB8]+0x38`, kind 3 → `+0xA8`,
  other → 0. ORACLE's S9 is exact; OPUS's `+0xA8`-only statement is the kind-3 arm
  (not wrong, just narrower).

### +0x160 store census — extended **beyond** the claimed band (own falsification)

My .pdata-rooted image-wide scan finds **132** `+0x160` memory stores. Inside
`002F0000–0033FFFF` the set is exactly ORACLE's 14-site `EXPECT` list. Outside the band the
`movss` float stores are:

- `0023634A` — a `00265200` facing result cached on a *different* record type
  (parent object with `+0x10` inner context, `+0x15C`/`+0x174` neighbours). Bounded source —
  consistent with the conclusion even though it is a heading-flavour store the band-scoped
  census did not enumerate.
- `002EF229` — `003EC580(cx)` table element (`0x740`-stride), double-store to `+0x160`/`+0x164`
  — a vec2 pattern, not a heading.
- `006A0B13`, `00853289`, `00853344`, `00853590`, `008538E1`, `00853953` — all `+0x160/164/168`
  float3 maths on non-battle objects.
- All other out-of-band hits are dword/word/byte/qword writes — not heading-shape.

**No image-wide `+0x160` store writes an unbounded value onto a BattleUnit.** The records'
band scope is honestly declared; the expansion finds no counterexample, only the benign
`0023634A` facing cache.

### `003EC040` residue check (cross-package, from the SD-193 review)

SD-193 showed `003EC040` modes 0/1 return `cur ± step` unwrapped. Both its call sites were
inspected: `002E59ED` result → `0026C300` (stores the *int* `edx`, not the float — xmm6 is
callerside only), `00358E61` result → `0026B5A0`, which itself performs a
`x mod 360 − 180` wrap in its first 12 instructions before calling `0026B6A0`/`0026C090`.
No unwrapped store escapes.

### Script corpus (TSV sampled, 7,092 rows)

- Verbs: **7,092 × `setposparty`, zero `setposparty_mapjump`** ✓
- Constants: 5,229 `PUSHF` + 1,449 `PUSHII` = **6,678** ✓; max `PUSHII` = 0.0.
- Out-of-range constants: **171** once the authored π literal (153 × 3.141593) is excluded —
  135 × 4.712389 (3π/2), 18 × 3.926991 (5π/4), 9 × 4.363323, 9 × 5.846853 (`sav_b01` × 9
  languages, max 5.846853 = 335°) — the record's "171 = 19 per language" and its distinct-value
  list are exact.
- Variables: **279** `PUSHV` rows; 9 rows = `evt_t0505`'s `PUSHV:1:0000A8` accumulator
  (one site × 9 languages) — the claimed unbounded debug source.
- `getrotangzx` rows: **135** ✓.

## Findings

- **No defect.** Every load-bearing claim reproduced on the bytes or the corpus.
- Coverage note (not a defect): the `+0x160` census was band-scoped as declared; the
  image-wide expansion finds one additional *bounded* facing store (`0023634A`, different
  record type) and no unbounded writers. The conclusion is unchanged.
- OPUS's `+0xA8` single-writer line is narrower than ORACLE's S9 (which adds `0026B6A0` for
  the kind-1 `+0x38` arm) — complementary, not contradictory; both writers wrap.

## Limits carried over (as declared by the authors)

- Variable trace is one step / flow-insensitive; cross-image shared-class writes unmodelled.
- `evt_t0505` reachability in retail play is unresolved (runtime question).
- Executed runs are float32; NaN/Inf not examined.

**Verdicts: `OPUS-REQ-AUDITSPEC-SD184-0930` → ACCEPT; `ORACLE-REQ-AUDITSPEC-SD184-0930` → ACCEPT.**
