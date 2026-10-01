# Consumer-check record — SWE2-CONTRACT publish 2026-09-26 (second)

Publish scope: the `UQ-367` delivery-chain corrections on the glyph page plus the
ambient-slot-block coda, with index-file entries.

## Corrections carried

1. **`002E16B0` `edx` is a window-slot index, not a message type.** Supersedes the
   uncommitted sentence "`type == 7` swaps the arguments for a shared `020BF200`
   stream". Verified against the image before applying (FABLE's reading confirmed):
   `min(esi,7)` `cmovg` clamps at `002E16FF`/`002E1827`/`002E18FD`; `0215F200` is the
   eight-entry `0x68`-stride window-slot registry (`lea` `002E170C`, `002E1830`); a
   whole-`.text` rip-relative census finds zero references into `020BF200`–`020BF300`;
   `002A35B0` at `002E1933` is reached only via old `byte[rbx+0x40]==-1` (`002E1811`)
   with `r8 = r13` = the caller's stream unchanged.
2. **"Authored resource data" rescoped.** The delivered stream is a `00264D60`
   message-table entry of the current actor-manager slot block `[02099D70]` (EF-3's
   canonical name; replaces "message pack"). The `+0xA0`/`+0xA8` table planter is
   unread — `0026C8C0`'s bind clears `+0xA0`/`+0xA8`/`+0xB0`/`+0xB8`/`+0x108`
   (`0026CC49`–`0026CC65`); `00264D60` returns the shared empty string `01CEB638`
   for absent table / out-of-range id.
3. **Ambient-slot mechanics (new, not a correction).** `002640C0` getter — 140 call
   sites; `00264050` push/pop installer — 8 verb-region sites, default `02099E10`,
   `mode<0` restores.

## Affected consumers

- `how-a-line-of-text-becomes-glyph-quads.md` — the owning page; both corrections
  applied in place, the superseded reading explicitly annotated.
- `_index/AUDIT-LOG.md`, `_index/PROGRAM-STATE.md` — the re-landed (uncommitted)
  DELIVERY-0925 entries repeated the wrong sentence; both annotated in place.
- `OPEN-QUESTIONS.md` `UQ-367` row — checked: carries only "OPEN", no stale claim.
- `the-script-to-native-calling-convention.md` EF-3 — checked: already names
  `02099D70` the actor-manager slot block; the coda adopts that name, no edit needed.

## Regression / control

- `verify_doc_addresses` on the page: 395 cited, 0 unconfirmed (new cites
  `002E16FF`/`002E1827`/`002E18FD`/`0215F200`/`002E1811`/`002E1933`/`01CEB638`/
  `0026C8C0`/`0026CC49`/`0026CC65`/`02099E10` all adjudicated).
- Zero-ref claim control: the same rip-census instrument positively finds
  `0215F200` twice in `002E16B0` — the negative on `020BF2xx` is instrument-valid.
- `check_questions`, `check_consistency`, `check_links` — clean except the
  pre-existing peer `_experiments/`/`candidates/` breaks.
