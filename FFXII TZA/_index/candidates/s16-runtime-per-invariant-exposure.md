# S-16 runtime: per-invariant stub exposure for EXP-145, which is an import bridge only (OPUS, 2026-09-25, block 294)

**Row:** S-16, spawn placement. AUDIT-SEM scored the runtime cell MIXED ("EXP-145 executes spawn placement
`00234AF0` in both modes … no per-invariant stub-exposure analysis yet"). The binding gap reads "no placement body
executed; `Y` unwritten and an unset slot is read". The contract is `05-Spawn-Encounter-Lifecycle/CONTRACT-spawn-placement.md`.
This note scores nothing.

## The one substitution in EXP-145, identified

EXP-145 (`evidence/spawn-placement-exec/check.py`) runs `00234AF0`, `00235330` / `00235340`, `003209C0` → `003DFD00`,
the probe `00234DA0`, the validator `00322C50`, both LCG draws, the sine table and the region transform `00325EA0`
as shipped bytes. The only scripted boundary is `0x861F02`, the `0031AC90` tail `jmp qword [008C2BD0]`.

**Correction to EXP-145's record.** It calls that cell "not a named import — encoded CRT pointer, file holds
`0x1CCED38`". The PE import directory resolves **`008C2BD0` to `api-ms-win-crt-math-l1-1-0.dll!atan2f`**. The file
value `0x1CCED38` is the RVA of that entry's hint/name record, which is how every unbound IAT slot looks on disk. The
same resolution gives `008C2B40` = `malloc` and `008C2B60` = `_aligned_malloc`, the database's known slots. So the
boundary is a **CRT import**, not an application function.

**The bridge is faithful to the import's contract.** The harness reads **`xmm0` as y and `xmm1` as x**, the registers
the shipped caller loaded, and returns `atan2(y, x)` in `xmm0`. It does not supply its own dx / dz, so the caller's
argument order is the one exercised. This is the same class of substitution as the imported-`memset` bridge the S-04
and S-10 analyses accepted.

## Per invariant

| inv. | executed by (EXP-145 case) | can the substitution reach it? |
|---|---|---|
| **I1** a negative window restores 300 | `win-neg` / `win-zero` / `win-pos` | **no** |
| **I2** the caller rejects negative, not zero | `fetch-direct`, `fetch-null`, `fetch-oob` | **no** |
| **I3** two exclusive modes, validated differently | point: `point-hit` / `point-arc-miss` / `point-band-*` / `point-coincident`. Area: `area-box-*` / `area-ellipse-hit` / `area-shape3` / `oldfmt-point` | **Point mode's arc test** takes the heading from `0031AC90`, which ends in the `atan2f` import: **import-class** exposure. The arc comparison, the band probe, both area draws and the region shapes are shipped code |
| **I4** only the leader is consulted | `null-leader`, `probe-allslots-fail` (the leader chain `003590D0` → `003588B0` is real) | **no** |
| **I5** an empty band is refused first | `empty-band` (fetch never called) | **no** |
| **I6** area mode leaves `out_observed` unwritten | area cases (producer side) | **no**. The consumer half (the automatic caller reading the slot) is **not executed** by EXP-145; that is coverage, not exposure |
| **I7** `Y` is not written | area cases: the `0xCD` stack fill replaced an authored `y = 7.5` (consumed into the contract at I7) | **no** |
| **I8** trig: a sine table, and `atan2(dx, dz)` as the inverse | the sine table `01F004E0` is read as shipped (area draws). The `atan2` half **is** the import | the `atan2` half is **import-class**. The table half is shipped code |

## For the scorer

- **No application stub reaches any invariant.** The single substitution is the `atan2f` CRT import, bridged from
  the caller's own argument registers with library semantics. It touches I3's point-mode arc and I8's inverse-trig
  half.
- **The binding-gap text is stale on two of its three clauses.**
  - "No placement body executed": EXP-145 executes `00234AF0` in both modes.
  - "`Y` unwritten": this is **confirmed behaviour** of the shipped code (I7, executed and statically read), not a
    missing piece of evidence.
  - "An unset slot is read": I6's consumer half is the one piece not executed.
- `live_game` is false.
