# DD owner re-status, batch 19: the @FTR, @FEF and FTE/FCT format pages to DOCUMENTED; SD-194 and SD-195 registered (OPUS, 2026-10-01)

SWE2-CONTRACT's DD batch 14 ([`swe2contract-ddres-b14-0930`](../swe2contract-ddres-b14-0930/README.md), `b14_checks.py`
317 PASS, FAILS 0) answered batch 10's proposed rows P1-P7 statically. It left two id-less rows for SWE2-DATA and four
proposed status lines for OPUS. FABLE (and with it DATA) is inactive, and the user authorized OPUS to do the work.

## Registered (OPUS for SWE2-DATA)

| id | question | status |
|---|---|---|
| SD-194 | the efx null-name request path: which `.efb` path `00377DC0` requests for the fields whose index names no map_ctrl package, and whether any such field loads | OPEN, runtime |
| SD-195 | what the u16 that @FTR bit 29 adds names | NO ADMISSIBLE SOURCE: nothing reads it, and the binder sets every bone's scale to 1.0 |

Both rows are inserted after SD-193. `check_questions --db` reports 0 / 0 for the cross-check and 0 cell-count
mismatches.

## Applied (OPUS)

CONTRACT's proposed status lines are applied, with the row ids filled in:

| page | status |
|---|---|
| `ftr-node-table.md` | PARTIAL -> DOCUMENTED (bit 29 is SD-195, NO ADMISSIBLE SOURCE; pointer added at the bit-29 finding) |
| `fef-and-motion-entries.md` | PARTIAL -> DOCUMENTED (which models a session loads, and the target-bearing arm's look, are runtime-only bounds on the page's claims) |
| `fte-fct-texture-colour-tables.md` | PARTIAL -> DOCUMENTED (what a co-drawn model sharing a texture key shows is a runtime-only bound) |
| `efx-and-efb-effect-containers.md` | stays PARTIAL on SD-194; its runtime row in §2c now names the id |

`documented_rule.py`: TALLY READY 2 + READY-WITH-POINTER 1 of 3 ([`documented_rule.out`](documented_rule.out)).

## A-drift, paired (OPUS)

The @FTR page makes `00200090` A (`@00200100`), a JsonBox member. `exact_remove.py` takes 55 -> 54, and the dated note
comes from `round9_notes.py`. `select_jsonbox.py` does not re-run at HEAD (EC7's batch-B note), so this is exact removal
only. Afterwards `adrift_report.py` reports 0 refused rows.

run: documented_rule.py 3 of 3 READY or READY-WITH-POINTER; adrift_report.py refused rows 0 (FAILS 0)

## Review (OPUS)

The owner read and the two registrations go to SWE2-AUDIT-SPEC. The registrations are noted to SWE2-DATA. SD-194 goes to
the runtime queue.
