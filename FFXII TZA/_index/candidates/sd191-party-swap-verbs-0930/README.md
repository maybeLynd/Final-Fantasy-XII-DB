# SD-191: flag B is down only during summon entry and exit and the special-attack sequence (OPUS, 2026-09-30)

Register row SD-191 was registered by SWE2-DATA (DD owner read batch 5, `b92561451`) on
[how-the-engine-chooses-3d-or-flat-movement.md](../../../06-Movement-And-Navigation/Movement-Mode-Selection/how-the-engine-chooses-3d-or-flat-movement.md)
section 7. It asks which scripted sequences use which party-swap verb pairs, and so when the flat-movement gate's flag
B (`02B40534`) is down in play.

BV-5 names the verbs:

- **Drop flag B:** `0x202` `disposepartywithoutcontrol`, `0x2A3` `duplicatepartyinfo_spattack`, `0x232`
  `capturepartyforsummon` and `0x191` `setpossummonspace`.
- **Raise flag B:** `0x195` `resumeposbattletarget`, `0x205` `changetosummonparty` and `0x2A4`
  `resumepartyinfo_spattack`.

**Evidence: a census of the shipped scripts.** The new kit tool
`Database/Tools/analysis-kit/gfz-scripts/script_verb_census.py` decodes every `.ebp` with FABLE's decoder. It
generalises the SD-160 census and names each calling script from the section's name pool (BW-5). The checker is
`sd191_check.py` (output `sd191_check.out`, `FAILS 0`); `sd191-census.out` is the census run, and
`sd191-calls-us.tsv` keeps the us copy's 82 calls.

## The answer (OPUS)

**C1–C3: where the verbs are.** 738 calls in 27 zone files, and the nine language copies agree in every file. The
verbs occur **only** in:

- the 26 summon files `sum_a`…`sum_m` × `0000` / `0001`, the 13 Espers;
- one special-attack file, `spc_z0000`.

No field or story script calls them.

| sequence | script | calls, in order | flag B |
|---|---|---|---|
| summon entry (13, `sum_x0000`) | `監督` (director) | `capturepartyforsummon` → `disposepartywithoutcontrol` → `setpossummonspace` → `changetosummonparty` | down from the capture until `changetosummonparty` |
| summon exit (13, `sum_x0001`) | `監督`, `進行監督`, `DIRECTOR`, or `終了` + `ＡＤ` (b, g, i) | one `setpossummonspace` and one `resumeposbattletarget` | down between them |
| special attack (`spc_z0000`) | `監督` | `duplicatepartyinfo_spattack` → `setpossummonspace` → `resumeposbattletarget` → `resumepartyinfo_spattack` | down from the duplicate until the resume |

**So in play, the flat-movement gate is closed only while a summon enters or leaves, and during the special-attack
sequence.** The script that raises the flag ends each window. Everywhere else flag B stays up, from its boot set by
`003B6ED0` (BV-5).

## Limits (OPUS)

- **Order is static.** It is the order of the calls in each function's bytecode, not a traced execution order.
  Branches inside the director scripts were not followed.
- **The exit ordering varies.** In `sum_e0001` the static order is `resumeposbattletarget` before
  `setpossummonspace`. For b, g and i the two calls sit in different scripts. Which runs first at run time is not
  traced for those files.
- **Which Esper each `sum_x` file is, and which special attack `spc_z0000` stages, is not mapped here.**
