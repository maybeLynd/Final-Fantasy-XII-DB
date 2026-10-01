# EXP-196 — Level-set `0030C650`, licence grant `00323910`, proximity scan `00234DA0` execution

**Status:** complete — **238/238 cases, stable across 3 independent runs,
byte-identical `result.json` (SHA256 `190871c7…`), zero unexpected faults.**
**Evidence class:** `NATIVE-REPLAY` (`live_game: false`). Shipped bytes executed
under Unicorn; synthetic fixtures disclosed below; none claim
initialized-gameplay reachability.
**Harness:** `_experiments/evidence/member-block-chain-exec/check.py` (extends
EXP-192..195; 202 inherited + 36 new `c650-*`/`g3910-*`/`d4da0-*` cases)
**Result:** `_experiments/evidence/member-block-chain-exec/result.json`
**Image authority:** FFXII TZA shipping EXE, SHA256
`73461D0896204B1C259C52F61AEF4EFBC95A2FFC388CADB36493D5D1D89721F8`.

## Scope

Executes the last three scripted boundaries of the battle-unit construction
contract — the level-set/level-up loop `0030C650`, the deep licence
grant/revoke `00323910`, and the member-slot proximity scan `00234DA0` — as
shipped bytes. With this package **every body on the contract's call surface
runs real**; the remaining scripted set is empty (only test-side stubs like
`00808C40` cookie and `00313F60`/`00324xxx` boundary hooks remain, disclosed
below).

Newly promoted real bodies include `002F9A60`/`002F9B20`/`002F9BD0` (growth
math), `00379CD0`→`00863BF0` (MT temper), `0035D8C0`/`002EACD0`/`003A1180`/
`002DF220`/`00329210`/`0046A690`/`003B02A0`/`001DBDB0` (level-up notify tail),
`00323D10` (grant eligibility), `00324280` (cross-slot licence scan),
`0030A310`/`00300B80`/`003008A0` (rank member chain), `0031E620`/`003A1960`
(distance), `003590D0` (notify-id read `d[022C7FE0]`).

## New executed facts

### `0030C650` — level-set / level-up (`rcx`=rec, `edx`=target, `r8`=flags)

- Level byte `b[rec+0x1C2]`; target clamps to `0x63`. At cap → immediate ret,
  no growth, no notify (`c650-max`).
- Per-level iteration: FOED level row `q[02EBF130]` (null → shipped null-deref
  fault @`0030C757` reading `b[0+0x1F]` — `c650-nolvl`), growth desc
  `q[02EBF108]` indexed by level (`grwrows`), then `2F9A60` HP, `2F9B20` MP,
  `2F9BD0` ×4 float stats `f[rec+0x10/14/18/1C]`.
- **`2F9A60` (HP)**: `cur + g` + jitter arm that **does** call `379CD0`→`863BF0`
  — correction to the earlier "dead branch" note: divisor `f[09136E4]` is
  negative, `cvttss2si` saturates to `INT_MIN`, so the modulus is the full
  tempered word and the bonus is `int(rem/100)`. With MT flag byte
  `b[02EB4234]`==0 the temper yields 0 → deterministic `cur+g` (hp 100→103,
  `c650-one`).
- **`2F9B20` (MP)**: divisor is `g*100` (positive) → `temper % int(g*100)`,
  bonus `int(rem/100)`. Verified byte-exact against a planted MT state:
  `mp = 50 + 5 + (temper(0x64) % 500)//100` (`c650-mp`).
- **`2F9BD0`**: float stat `+= g/128` (FOED `b[+0x1F/22/25/28]` growth bytes),
  observed 8→`+0.0625`, 16→`0.125`, 24→`0.1875`, 32→`0.25`.
- `b[rec+5]`==1 suppresses the growth bodies **and** the notify tail but still
  bumps the level and fires `30FED0(rec, 0)` once (`c650-b5`).
- `r8 & 2` suppresses the `46A690`/`35D8C0` notify tail only (`c650-hold`).
- Owner scan `31B860` runs **once per level** (`c650-multi`: 3 levels → 3×),
  while `46A690(rec,4)`, `3B02A0(d[objrow+8], objrow+8, 1, 0x71)` and
  `35D8C0(d[objrow+8])` fire once at the final level.
- Full tail (`c650-full`): `267330(0)` gate via `b[02098E10+0x10]` →
  `3A1180` serial resolve (`d[02AEF3FC]` key, rows `02AEEDC0+idx*0x18`,
  `w[+8]` match → `(w8<<9)|7` = `0x2007`) → `2DF220(0x2007)` →
  `1DBDB0(0x2007, 0x40, 0x7F)` → `329210` writes `d[0208D32C]`=ret.

### `00323910` — licence grant/revoke (`rcx`=rec, `edx`=id, `r8`=grant, `r9`=flags)

- Rejects `ret 0xFFFFFFFF` on null rec, `b[rec+5]`!=0, or `id >= d[abild+4]`.
- `r8==0` (revoke): `323D10` is **not** consulted — `btr` clears
  `b[rec+0x194+id>>3]` and `30FED0(rec,0x97)` still fires.
- Grant: `323D10` eligibility (`b[abilrow+6]` type arm — 1→`324280` cross-slot
  scan of the 7 `glob+8+i*0x1C8` rows; 2→`324020` popcount (≥3 rejects);
  ≥4→LP gate), then `bts` the licence bit and `d[rec+0x190] -= b[row+4]`
  (clamped at 0 — insufficient LP still grants and floors at 0, `g3910-lp0`).
- `r9&1` = silent grant: bit set, LP untouched (`g3910-silent`).
- Duplicate bit → `0xFFFFFFFF`, no LP change, no `fed0` (`g3910-dup`,
  `g3910-b6dup`).
- `id==0xE5`: after the bit set, `31B860` owner scan → `3105D0(objrow)`
  teardown on the owning object row (`g3910-e5`).
- Rank chain (`r14d` grant-only, `id <= 0x11`): `324020` popcount →
  `30A310(foerow@b[rec+4], popcount-1)` → `b[row+4] ∈ 0xD0..0xE1` →
  `30E600` resolve → `w[row+0x22]` → `300B80(member_id, 1, 0)` → real
  `3008A0` r9=1 arm bumping the class-1 word's low field `0x803→0x804`
  (`g3910-rank`). `b[lvrow+4]`==0 skips `300B80` entirely (`g3910-grant`).
- Grade arm (`id ∈ [0x12,0x1E)`): `308FF0(0, w[abilrow+8])` →
  `b[rec+0x20] = min(max(cur, ret), 3)` — upgrade-only (`g3910-grade`,
  `-cap`, `-hold`).
- Success always terminates in `30FED0(rec, 0x97)`.

### `00234DA0` — member-slot proximity scan (`rcx`=pos, `edx`=pmin, `r8`=pmax, `r9`=pout, `a5`=suppress)

- Iterates **all four** slots unconditionally — `31B810(slot)` resolves the
  `b[glob+0x5A5A+i*2]` map byte → OBJARR row (kind-0x17 bound `0..9`).
- Per candidate: `q[objrow+0x698]` rec → `(d[+0x64]|d[+0x3C]) & 0x80000003`
  nonzero → `313F60` alive gate (stubbed; `d4da0-gate` vs `-alive`) →
  `3273B0(d[rbx+8])` ctx-id check vs `d[022C7FE0]` (skipped when `a5`!=0 —
  call count drops 2→1, `d4da0-sarg`) → `265020` ctx triple (only when
  `b[ctx+3]>>5 ∈ {1,3}`, `d4da0-notrip`) → `31E620`/`3A1960` squared distance
  → bounds `f[pmin] <= d² <= f[pmax]` → `f[pout] = d²`, ret 1
  (`d4da0-hit`: pos `{4,0,3}` vs `{1,0,2}` → `d²=10`).
- `d²` outside bounds → miss (`d4da0-min` 50, `d4da0-max` 5); all-FF map →
  ret 0, `31E620` never reached (`d4da0-empty`); second-slot hit verified
  (`d4da0-second`).

## Harness additions

- `grwd`/`grwrows`: `02EBF108` growth desc (`stride`/`off`/`count` +
  `(hp_g, mp_g)` per level row).
- `mt`: MT state `d[02EB4230]` idx + `02EB4234` flag + `words` arena — real
  `863BF0` tempering validated.
- `a11`: serial key `d[02AEF3FC]` + `02AEEDC0` rows (`idx`, `w8`, `wA`).
- `slotd`: `31B810`'s kind-0x17 descriptor count.
- `oar4`: OBJARR rows for the proximity scan (`id`, `cid`=`d[+8]`, `trip`,
  `b3`, `recd`).
- `mctxid`: `d[022C7FE0]` notify ctx id (corrected from `022C6FE0` — verified
  against `3590D0`'s raw disp bytes).
- `o324020_ret`/`a308ff0_ret`/`s313f60_ret`/`b1dbdb0_ret`: boundary return
  fixtures; `d138`/`d138_rows`; `cls1words` class-1 member table;
  `abild`/`abil_rows` licence desc.
- Fixture fix: `oar4` no longer clobbers `OBJCNT` planted by `objlink`
  (count is now `max` of all sources).

## Disclosed scripted boundaries

`00808C40` cookie, `00313F60` alive-gate, `00324020`/`00308FF0`/`00323D10`/
`00324280` are **dual-registered**: real for direct-entry cases, SCR-stubbed
(`o324020`/`a308ff0`/`l323d10`/`l324280` tags) when mid-run callees so caller
branches can be steered — stubs return fixture values, never claim native
behavior. `00300B80` is scripted at its tail (`a08a0` delegates to real
`3008A0`). Null-desc faults (`c650-nolvl` @`0030C757`) are shipped behavior
under the disclosed fixture.

## Cases (36 new)

`c650-*` (9): `max` (at-cap early ret), `one` (full single level + notify
tail), `hold` (`r8&2` tail suppress), `multi` (3 levels, per-level `31B860`),
`b5` (growth suppress, level still bumps), `nolvl` (null FOED fault),
`clamp` (target 0xFF → 0x63), `mp` (MT-verified MP jitter), `full`
(serial→`2DF220`→`329210` tail).
`g3910-*` (17): `null`/`b5`/`badid` rejects, `grant`, `lp0` (LP floor),
`silent` (r9&1), `dup`, `revoke`, `e5` (owner teardown), `rank` (`300B80`→
real `3008A0`), `grade`/`-cap`/`-hold` (`b[0x20]` upgrade≤3),
`b6ok`/`b6dup`/`b6cap`/`b6t4` (`323D10` type arms 1/2/≥4).
`d4da0-*` (10): `empty`, `hit` (d²=10, `pout` write, ret 1), `sarg` (a5
suppresses `3273B0`), `cid` (ctx-id miss), `gate`/`alive` (`313F60` arm),
`min`/`max` (bounds), `notrip` (`b3>>5`==0 → no triple), `second` (slot 1).
