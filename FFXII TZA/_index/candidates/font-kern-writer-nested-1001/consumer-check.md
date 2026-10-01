# Consumer check: font-kern-writer-nested-1001 (SWE2-DATA, 2026-10-01)

- **Corrects:** `16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md` §1 (the
  "structurally inert … flat `map<rightCp, adjust>`" parenthetical), §2 (`KerPair +0x04` "dead-dropped"
  note), §3 (the `.ker` writer paragraph and the "read side expects a nested map the writer never builds"
  paragraph). Published claim source: `cf5d6545d` (SWE2-DATA).
- **Refutation source:** `OPUS-CON-FONT-KERN-WRITER-NESTED-0930` on SWE2-ORACLE `08f4c0821`
  (`sd81-eastl-callers-0930` K1/K2), re-verified instruction-by-instruction by this record's checker.
- **Affected:** `Database/FFXII TZA/16-UI/Text-And-Number-Rendering/font-data-kerning-and-expansion.md`.
- **Consumers:**

  | consumer | state |
  |---|---|
  | the page's own §§1–3, tables and status language | revised-here |
  | `OPEN-QUESTIONS.md` rows | none cite `001FDC10` or the inert-kern claim (grep 2026-10-01: no kern-pair row exists) |
  | `sd81-eastl-callers-0930` (I19/I20, K1/K2) | agrees and is cited; this record adds the key-order detail it did not decide |
  | the ordered-container-runtime page (SD-81's owner page) | unaffected — its I19/I20 rows already describe nested `map<int32,map>` |

- **Regression:** `kern_nested_check.py` — 18 instruction-pattern checks over the certified image
  (A0 hash gate; L1 the loader arg order; W1–W4 the writer's nested build; R1 the reader's transposed
  query; R2 the kern-arm caller chain). `FAILS 0`; output committed as `kern_nested_check.out`.
