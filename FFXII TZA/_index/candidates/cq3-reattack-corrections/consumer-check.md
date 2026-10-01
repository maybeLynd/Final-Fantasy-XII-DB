# Consumer-check record: CQ-3 re-attack corrections (SWE2-AUDIT-SEM, 2026-09-27)

Under `FRONTIER-RT-AUDITSEM-PROVENANCE-STAMPS` the ten documents carrying
`last_pass_state: reverification-against-current-parent` were re-attacked for
real: every size claim re-derived against the GN160 name/size set
(`Database/Tools/work/graph/functions.tsv`), and every discrepancy read from
the shipping bytes. 117 claims checked; two were wrong.

## What was corrected

affected: `Database/FFXII TZA/03-World-Area-Field/Weather/weather-apply-and-environment-materialization.md`
affected: `Database/FFXII TZA/08-Combat-Formula/Weather-Terrain-Element-Scaling/weather-terrain-element-scaling.md`
corrects: row CQ-3 register debt — two claims found false under re-attack.

| consumer | what it said | state |
|---|---|---|
| `weather-apply-and-environment-materialization.md` (exclusive-subtree table) | "`00394130` (5 B) — `jmp 0023A110` thunk" | revised-here — `00394130` is a 530-B body dispatching on `dword[rdx]`; it reaches `0023A110` by `call` at `003942F9`; no `jmp`-route to `0023A110` exists in the image |
| `weather-terrain-element-scaling.md` (triple-subtree table) | "`003210E0` (13 B)" | revised-here — the thunk is 9 B (`mov rcx,[rcx+0x10]` + `jmp 00263DD0`); 16-B padded slot |
| same page, `00321490`/`003214A0` thunk rows | both `jmp` thunks | agrees — verified byte-exact (5-B `jmp` each) |
| `weather-apply...` member row `0023A110` | "`byte[0208D455] = cl` weather-mode setter" | agrees — `0023A110` is `mov byte[0208D455],cl; ret` |
| CQ-3 register row | "10 documents remain stamped-not-verified" | agrees — the stamp debt was real; a true re-attack surfaced wrong claims. Stamps themselves untouched (CT-1 rule: no stamp edits) |

Nothing here was executed at runtime; all findings are NATIVE/STATIC reads of
the certified image (`73461d08…`).

Full audit trail:
`Database/Tools/work/SWE2-AUDIT-SEM/REVIEW-2026-09-27-goalgate-declaration-register-provenance.md`.
