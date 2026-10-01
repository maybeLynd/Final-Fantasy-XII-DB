# REVIEW — OPUS-REQ-AUDITSEM-REVIEW-ITEMS-AND-CON173 · SWE2-AUDIT-SEM 2026-09-29

Passes: `561f67cae` (equipment compat + shop ladders), `624e3534e` (CON-173 +
fragment-size sweep). Regressions re-run non-author:
falsify_equipment_compat (Q0–Q9) / falsify_shop_ladders (G0–G9) FAILS 0;
fragment_size_sweep re-run reproduces its adjudication list.
Image `73461D08…21F8`.

## CON-173 — verified

`functions.tsv` now carries `003204E0` = 255 B and `0030C650` = 570 B
(chained-fragment unions, not first-fragment sizes). Both cited calls stand:
`0030C836 E8 → 003A1180` and `0030C84B E8 → 002DF220` sit inside the extent.
(Note for the record: `0030C830` itself is mid-instruction — `FF B9` decodes
as the invalid `/7` form; the call boundaries at `0030C836`/`0030C84B` are
what matter and both verify.)

## Fragment sweep adjudication — verified

Four false positives re-checked: `0032E620` 75 B is the script-verb caller's
own size on the same line; `00399110` 16 B is a "16-byte records" phrase;
`0030E060` 57 B is the deliberate first-unwind-entry citation; `00248220`
85 B was already corrected to 190 B on the widget page 2026-09-15 — the
remaining UQ-185 row is stale-but-flagged and deferred on a SWE2-DATA
register claim (disclosed, not silently dropped). `00729A3A` correctly
routed to FABLE as a chained fragment of `00729920`, not edited by OPUS.

## Verdict

**ACCEPT** — both contract passes and the sweep adjudication.
