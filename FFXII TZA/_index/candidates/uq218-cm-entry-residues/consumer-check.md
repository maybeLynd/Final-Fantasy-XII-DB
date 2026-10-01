# Consumer check: `@FMC` op `0x28` re-read as the effect request lane (SWE2-DATA, 2026-09-30)

**Affected path:** `17-Presentation-Rendering/Model-And-Motion-Formats/fef-and-motion-entries.md`
(op-`0x28` table row + residue bullet + frontmatter), and the shared `OPEN-QUESTIONS.md`
UQ-218 row whose cell carries historical `~~` strikes next to the appended NARROWED block —
that co-occurrence is what the gate sees; the appended text itself strikes nothing.

**What changed (narrowing, not a strike):** the prior rows called `0x28` a "5-bit effect
request" whose authored values `{1,10}` were "unread". The full mechanism is now read on the
certified image (sha `73461D08…`):

- `00520720` → `003E6AA0(obj, dword+4)` — store `obj+0x304` bits 27–31, dirty bit 27 of `+0x294`.
- Dirty pass `00427DE0` → `003B3C00(handle=[obj+0x288], value)` — range-check `0..10`,
  validate handle vs the `0x38`-stride table `02E9D480` (`slot = handle & 0x3F`), then
  `0024FE70(effectCtx, lane)` (lane 0 short-circuits through `003B3480`).
- `0024FE70` — `def = [[ctx+0x130]+0x80]`; `byte[def+0xA+lane]` selects
  `dword[def+0x2C+4·map]` (resource id); `0020E600` resolves it.
- `00333280(childObj, id, lane)` — 16-slot child table, 0x170 alloc (`0036A190`), lane
  stamped `child+0x11`, `0046EE30`/`0046EFD0` construct+validate, `child+0x92` counter.

So `0x28` = "post request lane N to the bound effect instance" — an 11-entry per-effect
authored map, lane 0 = no request. The values `{1,10}` are per-effect lane indices, not a
global semantic enum. The `def` record class (`+0xA` map / `+0x2C` pool, plausibly a
`0x800`-chunk payload) stays an effect-format question, routed, not asserted.

**Consumers checked:**

- `fef-and-motion-entries.md` — updated this publish (row, residue, frontmatter). Agrees.
- `the-authored-presentation-command-handlers.md` op-`0x28` row — was the thin form
  "22 B — tail-calls `003E6AA0`" (correct but silent); enriched in the same publish. Agrees.
- `_index/candidates/uq218-cm-entry-residues/README.md` — updated this publish. Agrees.
- `OPEN-QUESTIONS.md` UQ-218 row — NARROWED block appended; residue tail updated. Agrees.
- `efx-and-efb-effect-containers.md` / `effect-element-type-dispatch.md` — searched; no
  prose claims the `0x28` operand's semantics, so nothing to reconcile. The open
  `def`-record-class question is theirs by ownership, noted not assigned.
- `render-event-selection-evidence.md`, `the-character-render-record-array.md`,
  `the-battle-unit-field-map.md`, `CONTRACT-efx-source-rebase.md` — searched for
  `003E6AA0`/`00520720`/`0024FE70`/`003B3C00`; none asserts a `0x28` operand semantics.

**Regressions:**

- `members/fmc_op28_census.py` (new, this publish) — corrected `co += len` walker over all
  `.cm`/`.ca` `@FMC` entries: total 115 commands, `{1:112}` in exactly 4 monster files
  (`m1043_10`/`m1044_10`/`m1132_10`/`m1133_10`, blocks `ready`/`knockback_s`/`knockback_l`/
  `c_turbo`/`ev_walk`/`avoid`), `{10:3}` in `m1143_10.ca` (`knockback_l` ×2, `dead` ×1),
  all values inside the `0..10` range-check. **FAILS 0** on the certified corpus.
- Mechanism addresses re-verified by disassembly against the shipping EXE
  (`003B3C00`/`0024FE70`/`00333280` bodies; canonical addresses already carry the image
  base).
