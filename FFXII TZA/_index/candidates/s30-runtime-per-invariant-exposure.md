# S-30 runtime: per-invariant stub exposure for EXP-092 (OPUS, 2026-09-25, block 301)

*Drafted by a delegated OPUS pass and reviewed before publication (block 301): its concrete address claims were spot-checked against the image; see the block-301 inbox entry for which.*

**Row:** S-30 shops and the bazaar. Runtime **MIXED** — *"EXP-092 executes the bazaar callees under isolated
original-code replay … no per-invariant stub-exposure analysis yet"*. Binding gap: *"types PARTIAL and nothing
executed — runtime is ASTRA/ORACLE's gap; the contract no longer binds it"*. Contracts (column 6 of
`important-subsystems.tsv`), both under `12-Items-Equipment-Shops-License/`:
- `CONTRACT-bazaar-unlock-and-purchase.md`: §4 is the refresh predicate's four clauses, the `flag |= 3`
  postcondition and *"the invariant that matters: bit 0 is never cleared anywhere in this family"*; the purchase
  steps are in §7;
- `CONTRACT-shop-stock-ladders.md`: SG-1..SG-7.

Evidence class: isolated original-code replay (Unicorn, `live_game: false`). This note scores nothing.

## Substitutions per record

Read from `_experiments/evidence/bazaar-callees-exec/check.py` (header, `CALLS`, `BODYSTUBS`, `World.__init__`,
`on_call`), `bodies.json` and `result.json`.

| record | runs as shipped | substituted |
|---|---|---|
| **EXP-092** (`evidence/bazaar-callees-exec/check.py`) | **16 bodies** (hashes in `bodies.json`): `0030B180` purchase, `0030B270` refresh, `0030B570` script-set, `0030ADC0` tally query, `00322C50` kind dispatcher, `00309440`, `003008A0`, `00309F30`, `002FD8D0`, `002FD970`, `002FD150`, `002FD780`, `002FD880`, `0020E600`, `00253690`, `00254EE0`. The **whole image** is mapped from the EXE's sections, so every reached callee is shipped code | **Application stubs: none** (`BODYSTUBS = []`; `on_call` only logs and never redirects). **Import bridges: none reached**; no IAT call is on these paths. **Fixtures:** registry slot `02EBF058` → synthetic `{+4 row count, +8 stride, +0xC rva}` plus goods rows; flag array `02EBF190` → base whose byte `idx` sits at `+idx+0x59C8`; resolver base `01F83530`; gil-bank object `02092758` (`+8`); family data pointers `fam+0x08` / `fam+0x20` for families 0/1/2 (runtime-null in the image; the counts `+0x3C` and handler pointers `+0x48`/`+0x50` are the shipped table's). **Hooked but unreached** (they would run real if reached): `002FD420`, `00316A50`, `0031EA90`. **Mutants:** 11, all detected |

## Per invariant

| invariant | executed by (case names from `check.py`) | can a substitution reach it? |
|---|---|---|
| bazaar refresh **clause 1**: not repeatable AND already unlocked rejects (`0030B33F`–`0030B34C`) | `ref-one-t`, `ref-repeat`, `ref-repeat-fail`, `seq-one-time`, `seq-one-time-trace` | **no.** No stubs; the fixture supplies row `+0x14` and flag bytes as inputs to a real comparison |
| **clause 2**: already available rejects (`0030B352`) | `ref-avail` | **no** |
| **clause 3**: all three thresholds zero rejects (`0030B35F`–`0030B36F`) | `ref-allzero`; mutant `0030B370` `je` → `jne` detected | **no** |
| **clause 4**: any loot's tally below its threshold; `-1` for sentinel / out-of-window, `0` for out-of-range index or no handler | `ref-tally0`, `ref-sentinel`, `ref-oob`, `ref-eq`, `ref-multi`, `tq-*`; mutant `0030B3DB` (`jl` → `jge`) detected. The tally is the **real** `+0x50` reader `002FD8D0`'s answer over fixture tables | **no substitution.** The fixture sets the tally values, which are inputs; the contract's claim is the comparison and the sentinel mapping, both executed as shipped |
| postcondition **`flag \|= 3`**, both bits at once (`0030B461`) | `ref-accept`; mutant `0030B467` (`3` → `1`) detected | **no** |
| **bit 0 is never cleared anywhere in this family** | all three flag writers executed: purchase `and 0xFD` (`0030B203`; mutant `0030B209` `0xFD` → `0xFF` detected), refresh `or 3`, script-set `(old & ~2) \| ((edx&1)<<1)` (`set-bit0free`) | **no.** "Anywhere" is a static census claim; the replay confirms each writer's mask, stub-free |
| (§7) purchase: gate `00322C50(0x12,id)` first, row from `id − 0xD000`, null row unguarded, three `003008A0(loot,0,1,3)` → byte-table absolute zero | `pur-*` (incl. `pur-nullrow` as an expected fault), `bnd-k12-*`, `sg-byte-zero` | **no** |
| shop ladders **SG-1..SG-7** (`002FAD40`, `002FA920`, `002FAE40`, `002536F0`, `00315390`) | **not executed.** No record under `_experiments/` executes these bodies; the only mention is EXP-137, which **excludes** `0x315390`. The contract's own §13 says "None" | coverage, not exposure |

## Fixture scope note

The fixture places the loot tally tables (`fam+0x20`) at independent heap addresses. The contract's §3 says the
sold tally lives "in the loot class's region B of the same block" (`BattleSystemState`), and FZ-3's save-survival
argument (§7) rests on that containment. The replay supplies that layout rather than measuring it. This bears on
§3/§7, **not** on any §4 clause, which reads the tally through the real handler whatever its address.

## Findings and contradictions

- **The binding gap is stale.** "types PARTIAL": the types cell reads MET (re-scored 2026-09-25). "nothing
  executed": EXP-092 executes the bazaar family stub-free. It stays true only for the shop-stock-ladders contract.
- **The bazaar contract misattributes the handler slot.** §13a ("`002FD150` — the class record's `+0x50`
  handler") and §15 (row "what the three scripted callees do": "The `+0x50` handler is `002FD150`") both say this.
  The shipped descriptor table `01EEBCC0` (read from the EXE, families 0/1/2) holds **`+0x48` = `002FD150`** and
  **`+0x50` = `002FD8D0`**. That agrees with EXP-092's own table and with `CONTRACT-inventory-class-storage.md` §2
  (mutate, packed = `002FD150`).
- **EXP-092's `check.py` header comment and its record disagree on `002FD8D0`'s `edx` arms.** The comment (lines
  37–38) reads 1 → `w>>0xA`, 2 → byte, 3 → `w&0x3FF`. Finding 1 of the record reads 1 → `w&0x3FF`, 2 → `w>>0xA`,
  3 → byte. **The shipped bytes agree with the record:**
  - `002FD939 and ecx,0x3FF` on `edx = 1`;
  - `002FD925 shr ecx,0xA` on `edx = 2`;
  - `002FD90F movzx ecx, byte [r8+rdx]` from `+0x20` on `edx = 3`.

  Only the comment is wrong. The harness's checks were not audited against it.
- **The bazaar contract's `entries:` front matter is stale against its own §2.** It lists `0030B1D0` and
  `0030B33F`. §2 says purchase is `0030B180` ("`0030B1D0` … is `0x50` into the body") and `0030B33F` is "the loop
  BODY, not the entry" of refresh `0030B270`.
- **The header comment says "IAT slots are zeroed".** The loader copies raw section bytes, and no code zeroes the
  IAT. The point is moot, since no case reaches an import. Not verified further.

## For the scorer

- EXP-092 has **no application stub and no import bridge**. The substitution set is **fixtures only**: registry,
  flag array, resolver base, bank object, family data tables.
- **Exposure: empty** for every executed bazaar §4 item (clauses 1–4, `flag |= 3`, bit-0 preservation) and for the
  §7 purchase steps.
- **Unexecuted:** SG-1..SG-7, i.e. the whole of `CONTRACT-shop-stock-ladders.md`. This is coverage, not exposure.
- One fixture decides a §3/§7 layout premise (where the tally bytes live), not a §4 claim.
- **Cross-row:** the same record runs `CONTRACT-inventory-class-storage.md`'s entries stub-free (S-29; see
  `s29-runtime-per-invariant-exposure.md`).
- `live_game` is false; the record is stable across two processes per its own text (`run2.log`, not re-run here).
