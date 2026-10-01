# Consumer-check record — SWE2-CONTRACT publish 2026-09-26 (third)

Publish scope: the `UQ-367` planter coda-2 on the glyph page, plus index entries.

## Corrections carried

1. **`00264050` is a borrow wrapper, not a push/pop installer.** Supersedes the
   committed coda's "installer" framing: it stores `arg`-or-default into
   `[02099D70]`, runs one call (`00358940` for `mode>=0`; the `003590D0`→`003588B0`
   cleanup pair for `mode<0`), then restores the prior block (`mov [02099D70], rbx`
   at `0026407E`/`0026409B`/`002640AA`). All eight call sites pass `(NULL, -1)` —
   every one borrows the *default* block `02099E10`; none installs a loaded block.
   Verified by re-decoding `00264050` and all eight call-site arg formations.
2. **The `+0xA0`/`+0xA8` message tables are INLINE in the slot block.** `00266AD0`
   plants them via an 8-way kind dispatch (`byte[block+3] & 0x1F`, jump table
   `00266BA4`): `+0x120`/`+0x140`/`+0x1A0`/`+0x4D8` per kind; `+0xA8 = +0xA0 +
   (0xC8|0xA0)` per `byte[01E0E329 + kind*4]`. This narrows the earlier
   "pointer into a loaded resource blob" reading — the planter wires pointers into
   the block's own storage; the *content* writer into `block+0x120`+ stays open.
3. New-only (not corrections): `00266BD0` = per-kind flag setter (`+0x1C` dword,
   `+0x14` bit7); planter callers `002665A9`/`002694A9`/`002694F8`; the
   `0026E060` borrow site fires `0x3000000|entry` through `002E9A60`.

## Affected consumers

- `how-a-line-of-text-becomes-glyph-quads.md` — owning page; coda-2 corrects
  coda-1's "installer"/"pack" phrasing and the "resource blob" framing in place,
  with the superseded claims annotated rather than silently rewritten.
- `the-script-to-native-calling-convention.md` EF-3 — consistent (names
  `02099D70` the actor-manager slot block; no edit needed).
- No other document states the `00264050` push/pop reading (greps for the
  function address and "message pack" phrasing — none outside the page).

## Regression / control

- `verify_doc_addresses`: 412 cited, 0 unconfirmed; `00266BA4` auto-adjudicated
  TABLE (jump-table target list verified: 8 entries → 4 distinct arms).
- Borrow-restore pairs confirmed pairwise: `0026407E`/`0026409B`/`002640AA`
  (restore `rbx`) inside `00264050`; `0026C472`/`0026C48D` and
  `0026E077`/`0026E0B7` direct-store pairs.
- `check_questions`, `check_consistency`, `check_links` — clean except the
  pre-existing peer `_experiments/`/`candidates/` breaks and two peer-drift
  EARLY items (`UQ-71`, `UQ-269`) not owned here.
