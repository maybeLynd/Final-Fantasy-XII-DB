# REVIEW: sd191-party-swap-verbs-0930

- **Package:** `sd191-party-swap-verbs-0930` (OPUS `f06af26c0`) + kit tool `script_verb_census.py`
- **Task:** `OPUS-REQ-AUDITSPEC-SD191-0930`
- **Reviewer:** SWE2-AUDIT-SPEC (independent of OPUS; own parser, not FABLE's decoder)
- **Verdict: ACCEPT**

## Controls re-run

Package copy `rerun_sd191_check_copy.py` → `rerun_sd191_check.out`: identical to committed
`sd191_check.out` (C1–C6 PASS, FAILS 0); regenerated census identical to `sd191-census.out`.
Package dir clean.

## Independent census — `own_census.py` / `own_census.out`

My own parser, no FABLE decoder, run over **all** `.ebp` in `D:\FFXII_TZA_extract` (not only
`event/`): section `@+0x80` (magic `0x8000000B`), directory `@sec+u32(+0x18)` (cnt × 0x30,
nameoff +0x00, codestart +0x08), linear decode with the `>0x63` anomaly rule and 3-byte
immediate ops `≥0x48`.

- **10,045** `.ebp` files, **0** decode anomalies, **0** unparseable directories —
  directory starts are complete coverage of these sections' code.
- **16,666,842** CALL-family instructions total (sanity magnitude).
- **Positive control:** `setposparty` (0x3B1) = **7,092** — byte-exact match to the
  independently-written SD-184 census. The instrument is proven.
- **Target verbs:** **738 calls**, exactly the claimed count. Per language: **82 × 9 = 738**;
  all nine copies agree in every file.
- **27 distinct zone paths**: `sum_a…sum_m` × `0000`/`0001` = 26 + `spc_z0000` = 27. **No
  field or story script calls them** — the "only" holds corpus-wide, not just `event/`.
- Per-verb split: `0x191`=243, `0x195`=126, `0x202`=117, `0x205`=117, `0x232`=117,
  `0x2A3`=9, `0x2A4`=9 — the pair structure (117 = 9 langs × 13 Espers; 9 = 1 file × 9)
  corroborates the sequence mapping.

## Raw-pattern bound

An undecoded sweep for `0x58/0x59/0x5D/0x5E` + verb-id bytes found 1,369 candidates; the 631
extras inspected are false alignments — data-region hits before the first directory start
(e.g. `lus_f03` @0x2AE, `dgl_g01` @0x84BF) or mid-instruction bytes inside decoded spans
(e.g. `byu_a15` @0x1A0DC, not an instruction boundary). No real call site sits outside the
decoded function starts; undecoded pre-start regions hold data (a call there could not be a
function body the VM runs anyway).

## Ordering spot-checks (own decoder + name pool)

- `sum_a0000` `監督`: `capturepartyforsummon → disposepartywithoutcontrol →
  setpossummonspace → changetosummonparty` — the claimed entry order, exact.
- `spc_z0000` `監督`: `duplicatepartyinfo_spattack → setpossummonspace → resumeposbattletarget
  → resumepartyinfo_spattack` — the claimed special-attack order, exact.
- `sum_e0001` `DIRECTOR`: `resumeposbattletarget @1508` before `setpossummonspace @1635` —
  the declared exit-order anomaly reproduces; the record honestly carries it.

## Limits carried

- Static order ≠ runtime order for the three exit files where the calls sit in different
  scripts (declared).
- Esper ↔ `sum_x` mapping and which special attack `spc_z0000` stages are not asked.
- The parser decodes only from directory starts — proven complete by zero anomalies plus the
  raw-pattern bound.

**Verdict: ACCEPT** — the gate-down windows (summon entry/exit, special attack) are exactly as
claimed, on an independently written corpus parser with a reproducing positive control.
