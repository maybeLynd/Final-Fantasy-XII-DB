# Consumer check — SWE2CONTRACT-PUB-GLYPH-0928C (kind-0xD4 file identity + producer correction)

Publish scope: glyph page (`how-a-line-of-text-becomes-glyph-quads.md`),
`AUDIT-LOG.md`, `PROGRAM-STATE.md`, `ADDRESS-INDEX.md`, `SWE2-CONTRACT.md`,
this record.

## Corrections carried by this publish

1. **"kind-0xD4 resource supplies the message table" is rescoped.** `0xD4`
   is a request kind meaning "serve the permanently staged bootstrap pack":
   init `0032F430` (call site `00266DE6`) loads kind 8 / id `0x350` =
   `PS2Data\plan_master\<lang>\event\pre_z\pre_z0000\pre_z0000.ebp`
   (3,840 B, identical SHA256 across 9 locales; path resolved in all five
   embedded language arrays) into `[022C6F10]`/`[022C6D3C]`.
   `003304A0` is the **universal** post-load section installer — the
   `0xD4` arm runs it inline after memcpy; normal `0032E620` reads pass it
   as the completion callback.
2. **`pre_z0000.ebp` does not plant `slot+0xA0`.** Its `EBP2` header has
   `dword@4 = 0x14` but only `+0x10` nonzero (0x80 — the script section,
   `init` + `"00/00 00:00"` + `iwabuchi` + `pre_z0000.src`), installed by
   `0032F850` into per-request array `022C6C28[reqIdx]`. The message table
   is the `+0x18` section of *other* packs (verified on
   `alc_a0100.ebp`: `+0x18 = 0x2440` → `{u32, {u16 off,u16 flags}[]}` +
   compiled-text streams). The issuer side is the `eventread`-verb family
   per the actor-manager record field map.
3. **`00264D60` bound refined:** `id < dword[table] >> 2`, `id & 0xFFFFFF`;
   entries `{u16 streamOffset, u16 flags}` at `table + i*4`.

## Consumers checked

- `how-a-line-of-text-becomes-glyph-quads.md` — corrected in place (coda-4).
- `PROGRAM-STATE.md` — PRODUCER-0928 entry annotated as corrected;
  `02099E10` slip in the INSTALLER-0926 entry fixed to `02098E10`.
- `the-actor-manager-record-field-map.md` — already documents the
  `0xD4`-to-slot-1 issuer (`0025DAE1`–`0025DAED`) and the `eventread`
  family; consistent, no edit needed.
- `file-size-tables-fst.md` — kind-8 = `event\*.ebp` family confirmed
  consistent; `0032E400` semantics match (`kind,id` → aligned size).
- OPEN-QUESTIONS UQ-367 row — carries no stale claim.
- Grep for other "kind-0xD4 supplies the table" repeats: none found
  outside the corrected files.

## Controls

- `0032E400` decode verified against `file-size-tables-fst.md` line 73
  (`022C51F0` override → `002DF960`/`0046DE70` `.fst` fallback, 0x40
  round-up, kind `0xFF` → −1).
- Path resolution positive control: all five language arrays yield the
  same `pre_z0000.ebp` path for id `0x350`; corpus SHA256 identical.
- `alc_a0100.ebp` `+0x18` section bytes inspected: entries `{u16,u16}`
  ascending offsets, compiled-text stream bytes at entry offsets.
